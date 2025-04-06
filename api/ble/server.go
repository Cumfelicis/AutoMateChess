package main

import (
	"fmt"
	"log"
	"net/url"

	"github.com/gorilla/websocket"
	"github.com/paypal/gatt"
)

var wsConn *websocket.Conn

// Connect to WebSocket server
func connectToWebSocket() error {
	// Define the WebSocket URL (replace with your server URL)
	serverURL := "ws://localhost:8080" // Replace with your Python WebSocket server URL

	// Parse the WebSocket URL
	u, err := url.Parse(serverURL)
	if err != nil {
		return fmt.Errorf("invalid WebSocket URL: %v", err)
	}

	// Connect to the WebSocket server
	conn, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		return fmt.Errorf("failed to connect to WebSocket server: %v", err)
	}

	// Save the connection for later use
	wsConn = conn
	return nil
}

// Send data to the WebSocket server
func sendDataToWebSocket(data []byte) error {
	if wsConn == nil {
		return fmt.Errorf("WebSocket connection is not established")
	}
	// Send the data to WebSocket
	err := wsConn.WriteMessage(websocket.TextMessage, data)
	if err != nil {
		return fmt.Errorf("failed to send message: %v", err)
	}
	return nil
}

func main() {
	// Connect to WebSocket server
	err := connectToWebSocket()
	if err != nil {
		log.Fatalf("Error connecting to WebSocket: %v", err)
	}
	defer wsConn.Close()

	// Setup BLE server
	d, err := gatt.NewDevice(gatt.DefaultClientOptions...)
	if err != nil {
		log.Fatalf("Failed to open device, err: %s", err)
	}

	// Register handlers
	d.Handle(
		gatt.CentralConnected(func(c gatt.Central) { fmt.Println("Connect: ", c.ID()) }),
		gatt.CentralDisconnected(func(c gatt.Central) { fmt.Println("Disconnect: ", c.ID()) }),
	)

	// When Bluetooth state changes, configure the service and characteristics
	onStateChanged := func(d gatt.Device, s gatt.State) {
		fmt.Printf("State: %s\n", s)
		switch s {
		case gatt.StatePoweredOn:
			// Create a new service with characteristics
			service := gatt.NewService(gatt.MustParseUUID("0000180f-0000-1000-8000-00805f9b34fb"))
			characteristic := service.AddCharacteristic(gatt.MustParseUUID("00002a19-0000-1000-8000-00805f9b34fb"))
			characteristic.HandleWrite(func(c gatt.ClientCharacteristic, data []byte) {
				fmt.Printf("Received data from client: %s\n", string(data))

				// Send data to WebSocket server
				err := sendDataToWebSocket(data)
				if err != nil {
					fmt.Println("Failed to send data to WebSocket:", err)
				}
			})

			// Add service to the device and start advertising
			d.AddService(service)
			d.AdvertiseNameAndServices("GoBLE", []gatt.UUID{service.UUID()})
		default:
		}
	}

	// Initialize the device with the onStateChanged callback
	d.Init(onStateChanged)

	// Keep the program running to allow BLE communication
	select {}
}
