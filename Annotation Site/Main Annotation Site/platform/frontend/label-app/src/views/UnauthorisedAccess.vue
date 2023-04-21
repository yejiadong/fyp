<template>
<section class="ftco-section">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="login-wrap p-4 p-lg-5 w-100">
                    <div class="spinner-grow text-danger" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h2>Authorised Access! Please make sure you access the annotation page from the home page with the database id and access key correctly filled in.</h2>
                    <button @click="homepage" type="submit" class="form-control btn btn-dark submit px-3 home-button mt-3">
                        <span class="badge text-bg-light ml-3 annotate-next">
                            Back to Home
                        </span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</section>
</template>

<script>
export default {
    name: 'Unauthorised',
    data() {
        return {}
    },
    methods: {
        homepage() {
            this.$router.push({ name: 'homepage' });
        },
    }
}
</script>
<style scoped>
.home-button {
    width: 300px;
    height: 55px;
    font-size:30px;
}
</style>
