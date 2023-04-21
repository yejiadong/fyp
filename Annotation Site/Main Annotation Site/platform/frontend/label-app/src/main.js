import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js"
import "bootstrap/dist/js/bootstrap.js"
import "bootstrap";
/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
/* import specific icons */
import { faArrowCircleRight } from '@fortawesome/free-solid-svg-icons'
/* import specific icons */
import { faTimes } from '@fortawesome/free-solid-svg-icons'
/* import vue-toastify */
import Toast from "vue-toastification";
/* Import the toastify CSS */
import "vue-toastification/dist/index.css";

/* add icons to the library */
library.add(faArrowCircleRight)
library.add(faTimes)

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)
app.use(Toast);
app.use(pinia);
app.use(router, axios);
app.mount("#app");
