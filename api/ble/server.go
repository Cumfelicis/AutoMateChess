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
				fmt.Printf("Received data: %s\n", string(data)) // Or process bytes directly
				if notifier != nil {
					sendFragmentedMessage(notifier, "Ack: "+string(data))
				}
				return gatt.StatusSuccess
			}))
			char.HandleNotifyFunc(func(r gatt.Request, n gatt.Notifier) {
				notifier = n
				for !n.Done() {
					time.Sleep(time.Second * 10)
					sendFragmentedMessage(notifier, "Periodic server")
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
	const maxPayload = 17
	const maxChunks = 255

	totalChunks := byte((len(data) + maxPayload - 1) / maxPayload)
	if totalChunks > maxChunks {
		fmt.Println("Message too long to send via BLE fragments")
		return
	}

	for i := byte(0); i < totalChunks; i++ {
		start := int(i) * maxPayload
		end := start + maxPayload
		if end > len(data) {
			end = len(data)
		}
		payload := data[start:end]

		// Allocate a fresh buffer per chunk to avoid reuse issues
		chunk := make([]byte, 3+len(payload))
		chunk[0] = i
		chunk[1] = totalChunks
		chunk[2] = byte(len(payload))
		fmt.Println(string(chunk))
		copy(chunk[3:], payload)
		fmt.Println("Chunk: " + string(chunk))
		fmt.Println("Payload: " + string(payload))
		// Write and delay a little to avoid overloading BLE stack
		n.Write(chunk)
		time.Sleep(100 * time.Millisecond)
	}
}
