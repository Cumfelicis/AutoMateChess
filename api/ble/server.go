package main

import (
	"fmt"
	"log"
	"time"

	"github.com/paypal/gatt"
	"github.com/paypal/gatt/examples/option"
)

const maxPayload = 17
const maxChunks = 255

func main() {
	var notifier gatt.Notifier
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
				handleWriteFragmented(r, data)
				if notifier != nil {
					sendFragmentedMessage(notifier, "Ack: "+string(data))
				}
				return gatt.StatusSuccess
			}))
			char.HandleNotifyFunc(func(r gatt.Request, n gatt.Notifier) {
				notifier = n
				for !n.Done() {
					time.Sleep(time.Second * 10)
					sendFragmentedMessage(notifier, "Periodic server Message eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
				}
			})
			// Add and advertise
			d.AddService(svc)
			d.AdvertiseNameAndServices("GopherReceiver", []gatt.UUID{svc.UUID()})
		}
	}

	d.Init(onStateChanged)
	select {}
}

func sendFragmentedMessage(n gatt.Notifier, message string) {
	data := []byte(message)
	fmt.Println("data: " + string(data))
	const maxPayload = 17
	const maxChunks = 255

	totalChunks := byte(len(data)/maxPayload) + 1
	if totalChunks > maxChunks {
		fmt.Println("Message too long to send via BLE fragments")
		return
	}

	for i := byte(0); i < totalChunks; i++ {
		fmt.Println(i)
		start := int(i) * maxPayload
		fmt.Println("Start: ")
		fmt.Println(start)
		end := start + maxPayload
		fmt.Println("End: ")
		fmt.Println(end)
		if end > len(data) {
			end = len(data)
		}
		payload := data[start:end]
		fmt.Println("Payload: " + string(payload))
		chunk := make([]byte, 3+len(payload))
		chunk[0] = i
		chunk[1] = totalChunks
		chunk[2] = byte(len(payload))
		fmt.Println("Chunk0:" + string(chunk))
		copy(chunk[3:], payload)
		fmt.Println("Chunk: " + string(chunk))
		fmt.Println("Payload: " + string(payload))
		n.Write(chunk)
		time.Sleep(100 * time.Millisecond)
	}
}

type FragmentBuffer struct {
	buffers     map[byte][]byte
	totalChunks byte
	received    byte
}

var fragmentMap = make(map[string]*FragmentBuffer)

func handleWriteFragmented(r gatt.Request, data []byte) byte {
	if len(data) < 3 {
		fmt.Println("Invalid fragment")
		return gatt.StatusUnexpectedError
	}

	chunkID := data[0]
	totalChunks := data[1]
	payloadLen := data[2]
	payload := data[3:]

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
		delete(fragmentMap, clientID)
	}

	return gatt.StatusSuccess
}
