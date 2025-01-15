import 'package:auto_mate_chess/components/commons/challenge.dart';
import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:flutter/material.dart';
import '../../constants/tint.dart';

class Computer extends StatefulWidget {
  const Computer({super.key});

  @override
  State<Computer> createState() => _ComputerState();
}

class _ComputerState extends State<Computer> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Tint.background,
      child: Padding(
          padding: EdgeInsets.symmetric(
              horizontal: responsiveWidth(30, context),
              vertical: responsiveHeight(35, context)),
          child: GridView.count(
            primary: false,
            crossAxisCount: 3,
            children: const [
              Challenge(
                time: 300,
                increment: 3,
                mode: 'Blitz',
              ),
              Challenge(
                time: 300,
                increment: 5,
                mode: 'Blitz',
              ),
              Challenge(
                time: 420,
                increment: 3,
                mode: 'Blitz',
              ),
              Challenge(
                time: 600,
                increment: 5,
                mode: 'Rapid',
              ),
              Challenge(
                time: 600,
                increment: 10,
                mode: 'Rapid',
              ),
              Challenge(
                time: 900,
                increment: 5,
                mode: 'Rapid',
              ),
              Challenge(
                time: 900,
                increment: 15,
                mode: 'Rapid',
              ),
              Challenge(
                time: 1200,
                increment: 15,
                mode: 'Rapid',
              ),
              Challenge(
                time: 1500,
                increment: 30,
                mode: 'Rapid',
              ),
              Challenge(
                time: 5400,
                increment: 0,
                mode: 'Classical',
              ),
              Challenge(
                time: 5400,
                increment: 30,
                mode: 'Classical',
              ),
              Challenge(
                time: 6000,
                increment: 30,
                mode: 'Classical',
              ),
            ],
          )),
    );
  }
}
