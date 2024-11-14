// User.js
export default class User {
	username = 'username1';
	profile_image = 'media/silvietto.jpeg';
	player = 'Player1';
	password = '';
	friendlist = [];
	wins_pong = 0;
	loses_pong = 0;
	winrate_pong = 0;
	wins_tictactoe = 0;
	loses_tictactoe = 0;
	winrate_tictactoe = 0;
	matchistory_pong = [];
	matchistory_tictactoe = [];
	language = 'EN';

	constructor(){}
	fillData(data){
		if (!data || !data.user) {
			console.error('Data or data.user is undefined');
			return;
		}
		console.log("filling user data.")
		this.username = data.user.username;
		this.player = data.user.player;
		this.password = data.user.password;
		this.profile_image = data.user.profile_image;
		this.friendlist = data.user.friendlist;
		this.language = data.user.language;
		this.matchistory_pong = data.user.matchistory_pong;
		this.matchistory_tictactoe = data.user.matchistory_tictactoe;
		this.loses_pong = data.user.loses_pong;
		this.wins_pong = data.user.wins_pong;
		this.loses_tictactoe = data.user.loses_tictactoe;
		this.wins_tictactoe = data.user.wins_tictactoe;
		this.winrate_pong = data.user.winrate_pong;
		this.winrate_tictactoe = data.user.winrate_tictactoe;
	}
	changeLanguage(language){
		this.language = language;
	}
	resetData(){
		this.username = 'username1';
		this.player = 'Player1';
		this.password = '';
		this.profile_image = 'media/silvietto.jpeg';
		this.friendlist = [];
		this.language = 'EN';
		this.matchistory_pong = [];
		this.matchistory_tictactoe = [];
		this.loses_pong = 0;
		this.wins_pong = 0;
		this.loses_tictactoe = 0;
		this.wins_tictactoe = 0;
		this.winrate_pong = 0;
		this.winrate_tictactoe = 0;
		console.log("User data reset.")
	}
}