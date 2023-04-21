<template>
<section class="ftco-section">
    <div ref="administrator" class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 text-center mb-5">
                <h1 class="heading-section">Let's Label</h1>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex">
                    <div class="text-wrap p-4 p-lg-5 text-center d-flex align-items-center order-md-last">
                        <div class="text w-100">
                            <h2>Administrator Login</h2>
                            <p>Annotating instead?</p>
                            <a @click="scrollMeTo('annotator')" class="btn btn-white btn-outline-white">Annotate</a>
                        </div>
                    </div>
                    <Transition name="slide" mode="out-in">
                        <div v-if="login" class="login-wrap p-4 p-lg-5">
                            <div class="d-flex">
                                <div class="w-100">
                                    <h2 class="mb-4">Sign In</h2>
                                </div>
                            </div>
                            <p>If you are an administrator, sign in here.</p>
                            <form @submit.prevent="submitSignInForm" class="signin-form">
                                <div class="form-group mb-3">
                                    <label class="label" for="name">Email Address</label>
                                    <input type="text" v-model="signInEmail" class="form-control" placeholder="Registered Email Address" required>
                                </div>
                                <div class="form-group mb-3">
                                    <label class="label" for="password">Password</label>
                                    <input type="password" v-model="signInPassword" class="form-control" placeholder="Password" required>
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="form-control btn btn-primary submit px-3">Sign In</button>
                                </div>
                                <div class="form-group d-md-flex">
                                    <div class="w-100 text-md-right">
                                        <a href v-on:click.prevent="login = !login">Don't have an account? Sign up
                                            <font-awesome-icon icon="fa-solid fa-circle-arrow-right" /> </a>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div v-else class="login-wrap p-4 p-lg-5">
                            <div class="d-flex">
                                <div class="w-100">
                                    <h2 class="mb-4">Sign Up</h2>
                                </div>
                            </div>
                            <p>Sign up as an administrator by filling in the form.</p>
                            <form @submit.prevent="submitSignUpForm" class="signin-form">
                                <div class="form-group mb-3">
                                    <label class="label" for="name">Unique Email Address (Used for Sign In)</label>
                                    <input type="text" v-model="signUpEmail" class="form-control" placeholder="Registered Email Address" required>
                                </div>
                                <div class="form-group mb-3">
                                    <label class="label" for="password">Password</label>
                                    <input type="password" v-model="signUpPassword" class="form-control" placeholder="Password" required>
                                </div>
                                <div class="form-group mb-3">
                                    <label class="label" for="name">Organisation / Institution</label>
                                    <input type="text" v-model="organisation" class="form-control" placeholder="Organisation / Institution" required>
                                </div>
                                <div class="form-group mb-3">
                                    <label class="label" for="name">Description</label>
                                    <input type="text" v-model="description" class="form-control" placeholder="Input your designation / any other information.">
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="form-control btn btn-primary submit px-3">Sign Up</button>
                                </div>
                                <div class="form-group d-md-flex">
                                    <div class="w-100 text-md-right">
                                        <a href v-on:click.prevent="login = !login">Already have an account? Sign in
                                            <font-awesome-icon icon="fa-solid fa-circle-arrow-right" /> </a>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </Transition>
                </div>
            </div>
        </div>
    </div>
    <div ref="annotator" class="container annotator">
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex">
                    <div class="text-wrap p-4 p-lg-5 text-center d-flex align-items-center order-md-last">
                        <div class="text w-100">
                            <h2>Annotator Access</h2>
                            <p>Administrator?</p>
                            <a @click="scrollMeTo('administrator')" class="btn btn-white btn-outline-white">Go to Administrator Sign In</a>
                        </div>
                    </div>
                    <div class="login-wrap p-4 p-lg-5">
                        <div class="d-flex">
                            <div class="w-100">
                                <h2 class="mb-4">Annotate</h2>
                            </div>
                        </div>
                        <p>If you are an annotator, access your annotation tasks here.</p>
                        <form @submit.prevent="beginAnnotation" class="annotate-form">
                            <div class="form-group mb-3">
                                <label class="label" for="name">Database ID</label>
                                <input type="number" v-model="databaseId" class="form-control" placeholder="This should be an unique number." required>
                            </div>
                            <div class="form-group mb-3">
                                <label class="label" for="password">Annotation Password</label>
                                <input type="password" v-model="annotationPassword" class="form-control" placeholder="Password" required>
                            </div>
                            <div class="form-group mb-3">
                                <label class="label" for="name">Annotator Email Address</label>
                                <input type="text" v-model="annotatorEmail" class="form-control" placeholder="Please fill in your unique email address to identify you." required>
                            </div>
                            <div class="form-group">
                                <button type="submit" class="form-control btn btn-primary submit px-3">Start Annotation</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
</template>

<script>
import axios from "axios";
import { useVuelidate } from '@vuelidate/core';
import { required, email } from '@vuelidate/validators';
import { useUserStore } from "../stores/user";
import { useToast } from "vue-toastification";
const domain = "";
export default {
    setup() {
        // Get toast interface
        const toast = useToast();
        // Set up Pinia User store
        const store = useUserStore();
        store.initializeUserStore();
        const token = store.token;
        if (token) {
            axios.defaults.headers.common['Authorization'] = "Token " + token
        } else {
            axios.defaults.headers.common['Authorization'] = ""
        }
        return { store, toast, v$: useVuelidate(), }
    },
    name: 'Home',
    data() {
        return {

            login: true,
            signInEmail: "",
            signInPassword: "",
            signUpEmail: "",
            signUpPassword: "",
            organisation: "",
            description: "",

            databaseId: "",
            annotationPassword: "",
            annotatorEmail: "",

        }
    },
    validations() {
        return {
            signInEmail: { required, email },
            signUpEmail: { required, email },
            signInPassword: { required },
            signUpPassword: { required },
            organisation: { required },
        }
    },
    methods: {
        scrollMeTo(refName) {
            var element = this.$refs[refName];
            var top = element.offsetTop;
            window.scrollTo(0, top);
        },
        async submitSignInForm(e) {
            this.v$.signInEmail.$touch();
            this.v$.signInPassword.$touch();
            if (this.v$.signInEmail.$invalid) {
                this.toast.error("Please check that you have inputed a valid email address.")
                return
            } else if (this.v$.signInPassword.$invalid) {
                this.toast.error("Please check that your password is not left blank.")
                return
            }
            const formData = {
                password: this.signInPassword,
                email: this.signInEmail,
            }

            axios
                .post(`${domain}/api/v1/token/login`, formData)
                .then(response => {
                    console.log(response)
                    const token = response.data.auth_token
                    axios.defaults.headers.common['Authorization'] = "Token " + token
                    // Get userid created
                    const emailData = {
                        email: this.signInEmail,
                    }
                    axios.get(`${domain}/api/v1/users/me`, emailData).then(response => {
                        this.store.setToken(token, response.data.id, this.signInEmail, response.data.institution)
                        this.$router.push({ name: 'dashboard' })
                    }).catch(error => {
                        console.log(error)
                        // Request was made and server responded unfavourably
                        if (error.response) {
                            // Authentication Error, redirect back to homepage
                            if (error.response.status === 401) {
                                //Reentry code, clear local storage
                                this.store.removeToken();
                                this.$router.push({ name: 'homepage' })
                            } else {
                                this.toast.error(error.response.data.non_field_errors[0]);
                            }
                        }
                        // Request was made but no response received
                        else if (error.request) {
                            this.toast.error("Received no response from the server. Please try again.");
                        }
                        // Something else happened
                        else {
                            this.toast.error("Sorry, an unknown error occurred. Please try again.");
                        }
                    })
                })
                .catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    if (error.response) {
                        if (error.response.status === 401) {
                            //Reentry code, clear local storage
                            this.store.removeToken();
                            this.$router.push({ name: 'homepage' })
                        } else {
                            this.toast.error(error.response.data.non_field_errors[0]);
                        }
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
        async beginAnnotation(e) {
            const annotationData = {
                databaseId: this.databaseId,
                accessKey: this.annotationPassword,
                annotationEmail: this.annotatorEmail,
            }

            axios
                .post(`${domain}/api/v1/database/annotation/check/`, annotationData)
                .then(response => {
                    console.log(response.data)
                    if (response.data.validated == true) {
                        this.store.setAnnotator(this.annotatorEmail, this.databaseId)
                        this.$router.push({ name: 'annotate' })
                    } else {
                        this.toast.error("Invalid access key specified.");
                    }
                })
                .catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    if (error.response) {
                        this.toast.error(error.response.data.detail);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })


        },
        submitSignUpForm(e) {
            this.v$.signUpEmail.$touch();
            this.v$.signUpPassword.$touch();
            this.v$.organisation.$touch();
            if (this.v$.signUpEmail.$invalid) {
                this.toast.error("Please check that you have inputed a valid email address.")
                return
            } else if (this.v$.signUpPassword.$invalid) {
                this.toast.error("Please check that your password is not left blank.")
                return
            } else if (this.v$.organisation.$invalid) {
                this.toast.error("Please check that your organisation is not left blank.")
                return
            }
            const formData = {
                role: 1,
                institution: this.organisation,
                description: this.description,
                email: this.signUpEmail,
                password: this.signUpPassword,
            }

            axios
                .post(`${domain}/api/v1/users/`, formData)
                .then(response => {
                    this.toast.success("Successfully signed up. Please login.")
                    console.log(response)
                    this.login = true
                })
                .catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    if (error.response) {
                        this.toast.error(error.response.data.non_field_errors[0]);
                    }
                    // Request was made but no response received
                    else if (error.request) {
                        this.toast.error("Received no response from the server. Please try again.");
                    }
                    // Something else happened
                    else {
                        this.toast.error("Sorry, an unknown error occurred. Please try again.");
                    }
                })
        },
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.fa-circle-arrow-right:hover {
    color: red;
}

.slide-enter-active {
    transition: all 0.25s ease-out;
}

.slide-leave-active {
    transition: all 0.25s ease-in;
}

.slide-enter {
    transform: translate(100%, 0);
    opacity: 0;
}

.slide-leave-to {
    transform: translate(-100%, 0);
    opacity: 0;
}

.annotator {
    margin-top: 50px;
}

.temporal-highlight {
  background-color: yellow;
}

@import '../assets/css/homepage.css';
</style>
