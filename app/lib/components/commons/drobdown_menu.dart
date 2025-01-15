import 'package:auto_mate_chess/components/utils/responsive_utils.dart';

import 'package:auto_mate_chess/constants/tint.dart';
import 'package:flutter/material.dart';

class DrobdownMenu extends StatefulWidget {
  final dynamic value;
  final Function(dynamic) onChange;
  final List<DropdownMenuItem> items;
  const DrobdownMenu(
      {super.key,
      required this.value,
      required this.onChange,
      required this.items});

  @override
  State<DrobdownMenu> createState() => _DrobdownMenuState();
}

class _DrobdownMenuState extends State<DrobdownMenu> {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
          border: Border.all(
              color: Tint.background, width: responsiveWidth(3, context)),
          borderRadius:
              BorderRadius.all(Radius.circular(responsiveWidth(8, context)))),
      child: DropdownButton(
          padding: EdgeInsetsDirectional.symmetric(
              horizontal: responsiveWidth(15, context)),
          elevation: 0,
          dropdownColor: Tint.primary,
          underline: Container(
            decoration:
                BoxDecoration(border: Border.all(color: Tint.background)),
          ),
          value: widget.value,
          items: widget.items,
          onChanged: widget.onChange),
    );
  }
}
