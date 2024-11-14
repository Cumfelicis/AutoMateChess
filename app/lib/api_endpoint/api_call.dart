import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:io';

const String apiUrl = '192.168.178.64:5000';

Future<http.Response> getPost(String route) async {
  print('test1');
  Uri url = Uri.http(apiUrl, route);
  http.Response response = await http.get(url);
  print('test2');
  print('Response status: ${response.statusCode}');
  print('Response body: ${response.body}');
  return response;
}
