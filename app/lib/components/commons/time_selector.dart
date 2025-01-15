import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';

class TimeSelector extends StatefulWidget {
  final dynamic value;
  final Function(dynamic) onChange;
  final double min;
  final double max;
  final int divisions;
  const TimeSelector(
      {super.key,
      required this.divisions,
      required this.max,
      required this.min,
      required this.onChange,
      required this.value});

  @override
  State<TimeSelector> createState() => _TimeSelectorState();
}

class _TimeSelectorState extends State<TimeSelector> {
  @override
  Widget build(BuildContext context) {
    return Slider(
        value: widget.value,
        min: widget.min, // Minimum 5 minutes
        max: widget.max, // Maximum 100 minutes
        divisions:
            widget.divisions, // 570 steps for precision (10 sec intervals)
        activeColor: Tint.background,
        onChanged: widget.onChange);
  }
}
