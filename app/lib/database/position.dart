import 'package:hive/hive.dart';

part 'position.g.dart';

@HiveType(typeId: 1)
class Position {
  @HiveField(0)
  String name;

  @HiveField(2)
  String fen;

  Position({required this.name, required this.fen});
}
