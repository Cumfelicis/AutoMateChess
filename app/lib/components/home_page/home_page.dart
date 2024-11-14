import 'package:auto_mate_chess/components/commons/chess_board/board.dart';
import 'package:flutter/material.dart';
import '../computer/computer.dart';
import '../../constants/tint.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int navBarIndex = 1;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        bottomNavigationBar: BottomNavigationBar(
          backgroundColor: Tint.background,
          elevation: 0.0,
          items: const [
            BottomNavigationBarItem(
                icon: Icon(Icons.person_search), label: 'online'),
            BottomNavigationBarItem(
                icon: Icon(Icons.psychology), label: 'computer'),
            BottomNavigationBarItem(
                icon: Icon(Icons.calculate), label: 'training')
          ],
          currentIndex: navBarIndex,
          onTap: (value) => setState(() {
            navBarIndex = value;
          }),
        ),
        body: navBarIndex == 0
            ? Container(
                color: Tint.background,
                child: const Board(
                  fen:
                      'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                ))
            : navBarIndex == 1
                ? const Computer()
                : navBarIndex == 2
                    ? Container(
                        color: Colors.black,
                      )
                    : Container());
  }
}
