#include <bits/stdc++.h>
using namespace std;
void solve(int n) {
	vector<int> path = { 0 };
	for(int i = 1; i <= n; i++) {
		if(i & 1) {
			for(int j = -i + 3; j < i; j += 2) path.push_back(j);
			path.push_back(i);
		}
		else {
			for(int j = i - 3; j > -i; j -= 2) path.push_back(j);
			path.push_back(-i);
		}
	}
	vector<int> revpath = path;
	reverse(revpath.begin(), revpath.end());
	if(n & 1) {
		for(int i = n - 2; i > -n; i -= 2) path.push_back(i);
	}
	else {
		for(int i = -n + 2; i < n; i += 2) path.push_back(i);
	}
	for(int i : revpath) path.push_back(-i);
	vector<int> board;
	for(int i = 0; i < n; i++) board.push_back(1);
	board.push_back(0);
	for(int i = 0; i < n; i++) board.push_back(2);
	cout << path.size() - 1 << endl;
	for(int i = 0; i < path.size(); i++) {
		if(i >= 1) swap(board[path[i - 1] + n], board[path[i] + n]);
		for(int j = 0; j < board.size(); j++) cout << board[j] << ' ';
		cout << endl;
	}
}
int main() {
	solve(9);
	return 0;
}