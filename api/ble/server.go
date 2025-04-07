package main

import (
	"fmt"
	"log"

	"github.com/paypal/gatt"
	"github.com/paypal/gatt/examples/option"
)

func main() {
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
				return gatt.StatusSuccess
			}))

			// Add and advertise
			d.AddService(svc)
			d.AdvertiseNameAndServices("GopherReceiver", []gatt.UUID{svc.UUID()})
		}
	}

	d.Init(onStateChanged)
	select {}
}
