new Vue({
    el: "#tournament_detail",
    data: {
        tournament: {},
        players: [],
        organizers: [],
        counter: 0,
        innerWidth: window.innerWidth
    },
    methods: {
        formatDateTime(datetimeStr) {
        const datetime = new Date(datetimeStr);
        const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const timeOptions = { hour: 'numeric', minute: 'numeric', hour12: true };
        const formattedDate = datetime.toLocaleDateString(undefined, dateOptions);
        const formattedTime = datetime.toLocaleTimeString(undefined, timeOptions);
        return `${formattedDate} ${formattedTime}`;
      }
    },
    created: function(){
        const vm = this;
        const parts = window.location.pathname.split('/');
        const tournamentUniqueId = parts[parts.length - 2];
        axios.get(`/api/tournaments/${tournamentUniqueId}/`).then((response) => {
            vm.tournament = response.data;
            vm.players = response.data.players;
            vm.organizers = response.data.organizers;
        })
    }
})