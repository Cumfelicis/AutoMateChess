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
          children: List.filled(
              12,
              const Challenge(
                timeControl: '1 + 0',
                mode: 'Bullet',
              )),
        ),
      ),
    );
  }
}
