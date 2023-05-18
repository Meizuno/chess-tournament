new Vue({
    el: "#tournaments",
    data: {
        lang: "",
        theme: "",
        tournaments: [],
        user: {}
    },
    methods: {
        formatDate(date) {
          return new Date(date).toLocaleDateString()
        }
    },

    created: function(){
        const vm = this;
        vm.lang = getCookie('lang');
        vm.theme = getCookie('theme');
        axios.get('/api/tournaments/').then((response) => {
            vm.tournaments = response.data.tournaments;
            vm.user = response.data.user;
        })

        console.log('Language:', this.lang);
        console.log('Theme:', this.theme);
    }
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}