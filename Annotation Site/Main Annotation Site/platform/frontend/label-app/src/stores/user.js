import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
    state: () => {
        return {
            token: "",
            email: "",
            userid: "",
            institution: "",
            isAuthenticated: false,

            annotatorEmail: "",
            annotatingDatabase: "",
            isAuthenticatedAnnotation: false,
        }
    },
    persist: {
        beforeRestore: (ctx) => {
          console.log('about to restore')
        }
      },
    actions: {
    // mutations can now become actions, instead of `state` as first argument use `this`
    initializeUserStore() {
        if (localStorage.getItem('token') && localStorage.getItem('userid') && localStorage.getItem('email') && localStorage.getItem('institution')) {
            this.token = localStorage.getItem('token')
            this.userid = localStorage.getItem('userid')
            this.email = localStorage.getItem('email')
            this.institution = localStorage.getItem('institution')
            this.isAuthenticated = true
        } else {
            this.token = ''
            this.userid = ''
            this.email = ''
            this.institution = ''
            this.isAuthenticated = false
        }
        if (localStorage.getItem('annotatorEmail') && localStorage.getItem('annotatingDatabase')) {
            this.annotatorEmail = localStorage.getItem('annotatorEmail')
            this.annotatingDatabase = localStorage.getItem('annotatingDatabase')
            this.isAuthenticatedAnnotation = true
        } else {
            this.annotatorEmail = ''
            this.annotatingDatabase = ''
            this.isAuthenticatedAnnotation = false
        }
    },
    setToken(token, userid, email, institution) {
        this.token = token
        this.userid = userid
        this.email = email
        this.institution = institution
        this.isAuthenticated = true
    },
    setAnnotator(annotateEmail, annotateDatabase) {
        this.annotatorEmail = annotateEmail
        this.annotatingDatabase = annotateDatabase
        this.isAuthenticatedAnnotation = true
    },
    removeToken() {
        this.token = ''
        this.userid = ''
        this.email = ''
        this.institution = ''
        this.isAuthenticated = false
    },
    removeAnnotator() {
        this.annotatorEmail = ''
        this.annotatingDatabase = ''
        this.isAuthenticatedAnnotation = false
    },
    // easily reset entire state using `$reset`
    clearUser () {
        this.$reset()
    }
    }
});