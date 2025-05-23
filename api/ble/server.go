package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/url"
	"sync"
	"time"

	"github.com/gorilla/websocket"
	"github.com/paypal/gatt"
	"github.com/paypal/gatt/examples/option"
)

const maxPayload = 17
const maxChunks = 255

func main() {
	var notifier gatt.Notifier
	client, err := NewWebSocketClient("ws://0.0.0.0:8080")
	client.SetNotifier(notifier)
	go client.listen()
	if err != nil {
		panic(err)
	}
	d, err := gatt.NewDevice(option.DefaultServerOptions...)
	if err != nil {
		log.Fatalf("Failed to open device, err: %s", err)
	}

	d.Handle(
		gatt.CentralConnected(func(c gatt.Central) { fmt.Println("Connect: ", c.ID()) }),
		gatt.CentralDisconnected(func(c gatt.Central) { fmt.Println("Disconnect: ", c.ID()) }),
	)

	onStateChanged := func(d gatt.Device, s gatt.State) {
		fmt.Println("State:", s)
		if s == gatt.StatePoweredOn {
			// Custom Service
			svc := gatt.NewService(gatt.MustParseUUID("12345678-1234-5678-1234-56789abcdef0"))

			// Writable Characteristic
			char := svc.AddCharacteristic(gatt.MustParseUUID("abcd"))
			char.HandleWrite(gatt.WriteHandlerFunc(func(r gatt.Request, data []byte) (status byte) {
				handleWriteFragmented(r, data, client)
				if notifier != nil {
					sendFragmentedMessage(notifier, jsonify("Ack", "Ack: "+string(client.lastMessage)))
				}
				return gatt.StatusSuccess
			}))
			char.HandleNotifyFunc(func(r gatt.Request, n gatt.Notifier) {
				go func(n gatt.Notifier) {
					fmt.Println("Notifier goroutine started")
					for {
						if n.Done() {
							fmt.Println("Notifier is done. Exiting loop.")
							break
						}
						fmt.Println("Sending periodic message...")
						sendFragmentedMessage(n, jsonify("msg", "Periodic server message"))
						time.Sleep(10 * time.Second)
					}
				}(n)

			})
			// Add and advertise
			d.AddService(svc)
			d.AdvertiseNameAndServices("GopherReceiver", []gatt.UUID{svc.UUID()})
		}
	}

	d.Init(onStateChanged)
	select {}
}

type Message struct {
	Event string      `json:"event"`
	Data  interface{} `json:"data"`
}

func jsonify(command string, data interface{}) string {
	msg := Message{
		Event: command,
		Data:  data,
	}

	jsonBytes, err := json.Marshal(msg)
	if err != nil {
		panic(err)
	}
	jsonString := string(jsonBytes)
	fmt.Println("json:" + jsonString)
	return jsonString
}

func sendFragmentedMessage(n gatt.Notifier, message string) {
	data := []byte(message)
	fmt.Println("Fragmented send of:", message)

	totalChunks := byte(len(data)/maxPayload) + 1
	if totalChunks > maxChunks {
		fmt.Println("Message too long to send via BLE fragments")
		return
	}

	for i := byte(0); i < totalChunks; i++ {
		if n.Done() {
			fmt.Println("Notifier done during send. Aborting.")
			return
		}
		start := int(i) * maxPayload
		end := start + maxPayload
		if end > len(data) {
			end = len(data)
		}
		payload := data[start:end]
		chunk := make([]byte, 3+len(payload))
		chunk[0] = i
		chunk[1] = totalChunks
		chunk[2] = byte(len(payload))
		copy(chunk[3:], payload)

		_, err := n.Write(chunk)
		if err != nil {
			fmt.Println("Write error:", err)
			return
		}
	}
}

type WebSocketclient struct {
	conn        *websocket.Conn
	mu          sync.RWMutex
	lastMessage string
	notifier    gatt.Notifier
}

func NewWebSocketClient(rawurl string) (*WebSocketclient, error) {
	u, err := url.Parse(rawurl)
	if err != nil {
		return nil, err
	}

	conn, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		return nil, err
	}

	client := &WebSocketclient{
		conn: conn,
	}

	return client, nil
}

func (c *WebSocketclient) SetNotifier(n gatt.Notifier) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.notifier = n
}

func (c *WebSocketclient) listen() {
	for {

		_, message, err := c.conn.ReadMessage()

		if err != nil {
			log.Println("WebSocket read error:", err)
			return
		}
		c.mu.Lock()
		c.lastMessage = string(message)
		n := c.notifier
		c.mu.Unlock()
		log.Println("WebSocket recieved:", c.lastMessage)
		if n != nil {
			log.Println("redirecting")
			sendFragmentedMessage(n, jsonify("ack", c.lastMessage))
		} else {
			print(n)
		}
	}
}

func (c *WebSocketclient) SendMessage(msg string) error {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.conn.WriteMessage(websocket.TextMessage, []byte(msg))
}

func (c *WebSocketclient) GetLatest() string {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return c.lastMessage
}

type FragmentBuffer struct {
	buffers     map[byte][]byte
	totalChunks byte
	received    byte
}

var fragmentMap = make(map[string]*FragmentBuffer)

func handleWriteFragmented(r gatt.Request, data []byte, c *WebSocketclient) byte {
	if len(data) < 3 {
		fmt.Println("Invalid fragment")
		return gatt.StatusUnexpectedError
	}

	chunkID := data[0]
	totalChunks := data[1]
	payloadLen := data[2]
	payload := data[3:]
	fmt.Println(len(payload))
	fmt.Println(int(payloadLen))
	if len(payload) != int(payloadLen) {
		fmt.Println("Payload length mismatch")
		return gatt.StatusUnexpectedError
	}

	clientID := r.Central.ID() // use client UUID to identify unique sessions

	buf, ok := fragmentMap[clientID]
	if !ok || chunkID == 0 {
		// Initialize buffer on first chunk or reset
		buf = &FragmentBuffer{
			buffers:     make(map[byte][]byte),
			totalChunks: totalChunks,
			received:    0,
		}
		fragmentMap[clientID] = buf
	}

	buf.buffers[chunkID] = payload
	buf.received++

	if buf.received == buf.totalChunks {
		// All chunks received
		var fullMessage []byte
		for i := byte(0); i < buf.totalChunks; i++ {
			fullMessage = append(fullMessage, buf.buffers[i]...)
		}
		fmt.Println("Reassembled message:", string(fullMessage))
		c.SendMessage(string(fullMessage))
		delete(fragmentMap, clientID)
	}

	return gatt.StatusSuccess
}
