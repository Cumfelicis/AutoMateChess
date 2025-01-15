import 'package:auto_mate_chess/components/utils/responsive_utils.dart';
import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';

class ChooseName extends StatefulWidget {
  final Function(String) onDecision;
  const ChooseName({super.key, required this.onDecision});

  @override
  State<ChooseName> createState() => _ChooseNameState();
}

class _ChooseNameState extends State<ChooseName> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: responsiveWidth(250, context),
      height: responsiveHeight(350, context),
      decoration: BoxDecoration(
        color: Tint.background,
        borderRadius: BorderRadius.circular(responsiveWidth(5, context)),
      ),
      child: Card(
        child: TextField(
            decoration: const InputDecoration(hintText: 'Enter Name'),
            onSubmitted: (name) {
              widget.onDecision(name);
              Navigator.of(context).pop();
            }),
      ),
    );
  }
}
