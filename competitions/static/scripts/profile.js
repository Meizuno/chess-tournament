new Vue({
    el: "#profile",
    data: {
        player: {},
        participant: [],
        organizer: []
    },
    methods: {
        redirectToTournament(uniqueId) {
            window.location.href = `/tournaments/${uniqueId}/`;
        }
    },
    created: function(){
        const vm = this;
        const parts = window.location.pathname.split('/');
        const playerUniqueId = parts[parts.length - 2];
        axios.get(`/api/profile/${playerUniqueId}/`).then((response) => {
            vm.player = response.data;
        });

        axios.get(`/api/tournaments/`).then((response) => {
            const tournaments = response.data.tournaments;

            vm.participant = tournaments.filter(tournament => {
                return tournament.players.some(player => player.unique_id === playerUniqueId);
            });

            vm.organizer = tournaments.filter(tournament => {
                return tournament.organizers.some(organizer => organizer.unique_id === playerUniqueId);
            });

        })
    }
})