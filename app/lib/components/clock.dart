import 'dart:async';
import 'package:auto_mate_chess/api_endpoint/WebSocket.dart';
import 'package:flutter/material.dart';

class Clock extends StatefulWidget {
  final bool color;
  final int time;
  final int increment;
  @override
  const Clock(
      {super.key,
      required this.color,
      required this.time,
      required this.increment});

  @override
  State<Clock> createState() => _ClockState();
}

class _ClockState extends State<Clock> {
  late Duration player1Time;
  late Duration player2Time;
  late int incrementSeconds;
  final webSocket = SOCKET;

  Timer? timer;
  bool isPlayer1Turn = true;

  void toggleTurn() {
    setState(() {
      if (isPlayer1Turn) {
        player1Time += Duration(seconds: incrementSeconds);
      } else {
        player2Time += Duration(seconds: incrementSeconds);
      }
      isPlayer1Turn = !isPlayer1Turn;
    });

    timer?.cancel();
    startTimer();
  }

  void startTimer() {
    timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        if (isPlayer1Turn) {
          if (player1Time > Duration.zero) {
            player1Time -= const Duration(seconds: 1);
          } else {
            timer.cancel();
          }
        } else {
          if (player2Time > Duration.zero) {
            player2Time -= const Duration(seconds: 1);
          } else {
            timer.cancel();
          }
        }
      });
    });
  }

  void pauseTimer() {
    timer?.cancel();
  }

  void resetTimer() {
    timer?.cancel();
    setState(() {
      player1Time = Duration(seconds: widget.time);
      player2Time = Duration(seconds: widget.time);
      isPlayer1Turn = true;
    });
  }

  String formatDuration(Duration duration) {
    String minutes = duration.inMinutes.toString().padLeft(2, '0');
    String seconds = (duration.inSeconds % 60).toString().padLeft(2, '0');
    return "$minutes:$seconds";
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  void initState() {
    player1Time = Duration(seconds: widget.time);
    player2Time = Duration(seconds: widget.time);
    incrementSeconds = widget.increment;
    webSocket.onMove = (move) {
      toggleTurn();
      print(move);
    };
    webSocket.startStream();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            child: GestureDetector(
              onTap: isPlayer1Turn ? toggleTurn : null,
              child: Container(
                color: isPlayer1Turn ? Colors.green[200] : Colors.grey[200],
                child: Center(
                  child: Text(
                    formatDuration(player1Time),
                    style: const TextStyle(fontSize: 48),
                  ),
                ),
              ),
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              ElevatedButton(onPressed: pauseTimer, child: const Text("Pause")),
              ElevatedButton(onPressed: resetTimer, child: const Text("Reset")),
            ],
          ),
          Expanded(
            child: GestureDetector(
              onTap: !isPlayer1Turn ? toggleTurn : null,
              child: Container(
                color: !isPlayer1Turn ? Colors.green[200] : Colors.grey[200],
                child: Center(
                  child: Text(
                    formatDuration(player2Time),
                    style: const TextStyle(fontSize: 48),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
