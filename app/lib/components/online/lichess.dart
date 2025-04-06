import 'package:auto_mate_chess/api_endpoint/WebSocket.dart';
import 'package:auto_mate_chess/components/utils/responsive_text.dart';
import 'package:flutter/material.dart';

class ChallengesPage extends StatefulWidget {
  @override
  _ChallengesPageState createState() => _ChallengesPageState();
}

class _ChallengesPageState extends State<ChallengesPage> {
  late List<dynamic> _challenges;
  bool _loading = false;
  final WebSocket websocket = SOCKET;

  @override
  void initState() {
    super.initState();
    _fetchChallenges();
  }

  Future<void> _fetchChallenges() async {
    setState(() => _loading = true);
    websocket.getLichessChallenges();
    await Future.delayed(const Duration(seconds: 1));
    _challenges = websocket.challenges;
    print(_challenges);

    setState(() => _loading = false);
  }

  Future<void> _acceptChallenge(String challengeId) async {
    websocket.startOnlineGame(formatChallenge(challengeId));
  }

  Map<String, dynamic> formatChallenge(String id) {
    return {'challenge_id': id, 'time': false, 'increment': false};
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const ResponsiveText("Lichess Challenges")),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _challenges.isEmpty
              ? const Center(child: ResponsiveText("No challenges available"))
              : ListView.builder(
                  itemCount: _challenges.length,
                  itemBuilder: (context, index) {
                    final challenge = _challenges[index];
                    print(challenge);
                    return ListTile(
                      title: Text(
                          "Challenge from ${challenge['challenger']['name']}"),
                      trailing: ElevatedButton(
                        onPressed: () => _acceptChallenge(challenge['id']!),
                        child: const ResponsiveText("Accept"),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: _fetchChallenges,
        child: Icon(Icons.refresh),
      ),
    );
  }
}
