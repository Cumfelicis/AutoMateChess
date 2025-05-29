import 'package:auto_mate_chess/api_endpoint/ble_communication.dart';
import 'package:auto_mate_chess/api_endpoint/communicator.dart';
import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final TextEditingController _xController = TextEditingController();
  final TextEditingController _yController = TextEditingController();
  final Communicator _communicator = CONNECTOR.communicator;

  void _sendX() {
    final x = _xController.text;
    print("Sending X: $x");
    _communicator.moveStepperX(x);
  }

  void _sendY() {
    final y = _yController.text;
    print("Sending Y: $y");
    _communicator.moveStepperY(y);
  }

  void _sendXY() {
    final x = _xController.text;
    final y = _yController.text;
    print("Sending X: $x, Y: $y");
    _communicator.moveMultistepper(x, y);
  }

  void _calibrate() {
    print("Calibrating...");
    _communicator.calibrateArray();
  }

  void _read() {
    _communicator.readBoard();
  }

  @override
  Widget build(BuildContext context) {
    final xFilled = _xController.text.isNotEmpty;
    final yFilled = _yController.text.isNotEmpty;

    return Scaffold(
      appBar: AppBar(title: const Text("Chess Robot Positioning")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _xController,
                    decoration: const InputDecoration(labelText: "X Position"),
                    keyboardType: TextInputType.number,
                    onChanged: (_) => setState(() {}),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: TextField(
                    controller: _yController,
                    decoration: const InputDecoration(labelText: "Y Position"),
                    keyboardType: TextInputType.number,
                    onChanged: (_) => setState(() {}),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (xFilled && !yFilled)
              ElevatedButton(
                onPressed: _sendX,
                child: const Text("Send X"),
              ),
            if (yFilled && !xFilled)
              ElevatedButton(
                onPressed: _sendY,
                child: const Text("Send Y"),
              ),
            if (xFilled && yFilled)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _sendXY,
                  child: const Text("Send X & Y"),
                ),
              ),
            const Spacer(),
            ElevatedButton.icon(
              onPressed: _calibrate,
              icon: const Icon(Icons.build),
              label: const Text("Calibrate"),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(50),
              ),
            ),
            ElevatedButton.icon(
              onPressed: _read,
              icon: const Icon(Icons.build),
              label: const Text("Read Board"),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(50),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
