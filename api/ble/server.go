package main

import (
	"fmt"
	"os"
	"time"

	"github.com/muka/go-bluetooth/api"
	"github.com/muka/go-bluetooth/bluez/profile/gatt"
)

const (
	serviceUUID        = "12345678-1234-5678-1234-56789abcdef0"
	characteristicUUID = "12345678-1234-5678-1234-56789abcdef1"
)

func main() {
	adapterID := "hci0"

	// Initialize Bluetooth adapter
	a, err := api.GetAdapter(adapterID)
	if err != nil {
		fmt.Println("Failed to get adapter:", err)
		os.Exit(1)
	}

	err = a.FlushDevices()
	if err != nil {
		fmt.Println("Flush failed:", err)
	}

	fmt.Println("Setting up BLE GATT server...")

	srv, err := gatt.NewServiceServer(adapterID, serviceUUID, true)
	if err != nil {
		panic(err)
	}

	charProps := gatt.CharProperties{
		UUID:  characteristicUUID,
		Flags: []string{"read", "write"},
	}

	char, err := srv.AddCharacteristic(charProps)
	if err != nil {
		panic(err)
	}

	char.OnWrite(func(value []byte) {
		fmt.Println("Received via BLE:", string(value))
	})

	char.OnRead(func() ([]byte, error) {
		msg := fmt.Sprintf("Hello from %s!", adapterID)
		return []byte(msg), nil
	})

	err = srv.Register()
	if err != nil {
		panic(err)
	}

	fmt.Println("BLE GATT server is running. Ready for connections!")
	for {
		time.Sleep(10 * time.Second)
	}
}
