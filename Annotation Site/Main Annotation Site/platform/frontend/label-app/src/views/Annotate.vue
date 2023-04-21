<template>
<section class="ftco-section">
    <div ref="administrator" class="container">
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex p-3">
                    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                        <li class="nav-item mr-auto" role="presentation">
                            <button class="nav-link active position-relative" id="annotating-label" type="button">Annotating Database: {{ annotating_database }}
                                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                                    {{ count }} claim
                                </span>
                            </button>
                            <h6 class="mt-0 pt-2 pl-3 pb-2 annotator"> Annotator: {{ annotator_email }}</h6>
                        </li>
                    </ul>
                    <button @click="homepage" type="submit" class="form-control btn btn-dark submit px-3 home-button ml-auto">
                        <span class="badge text-bg-light ml-3 annotate-next">
                            Back to Home
                        </span>
                    </button>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-10">
                <div class="wrap d-md-flex">
                    <template v-if="annotationTodo && count != 0">
                        <div class="login-wrap p-4 p-lg-5 w-100">
                            <div class="d-flex">
                                <div class="w-100">
                                    <span class="badge text-light topic-badge mb-3">Topic: {{ this.topic }}</span> <br />
                                    <p v-if="this.section == 0 || this.section == 1">Temporal parts of the claim and evidence are highlighted in yellow.</p>
                                    <p v-else>The relevant parts of the evidence are <strong>bolded.</strong></p>
                                    <span class="badge text-bg-primary claim-badge ml-1">Claim</span>
                                    <h3 class="mb-4 claim-text ml-1" ref="temporalListner">{{ sanitizeText(annotationTodo.content) }}</h3>
                                </div>
                            </div>
                            <div class="form-group mb-3 evidence-div p-2">
                                <span class="badge text-bg-primary claim-badge mb-3">Evidence ( {{ currentEvidenceCount + 1 }} out of {{ evidenceCount }} )</span>
                                <div class="d-flex">
                                    <div v-if="annotationTodo != null" class="w-100">
                                        <h5 class="mb-2 evidence-text" ref="temporalEvidence" :id=annotationTodo.evidences[currentEvidenceCount].id>{{ sanitizeText(annotationTodo.evidences[currentEvidenceCount].content) }}</h5>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-4 mt-4">
                                <div class="col-md-12 col-lg-12 annotation text-left">
                                    <template v-if="section == 0">
                                        <div class="form-group mb-1">
                                            <span class="badge text-bg-primary label-badge">Temporal Label</span>
                                        </div>
                                        <div class="btn-group w-100" role="group" aria-label="Basic radio toggle button group">
                                            <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio1" value=0 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="temporalbtnradio1">Supports</label>

                                            <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio2" value=1 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="temporalbtnradio2">Refutes</label>

                                            <input type="radio" v-model="temporalFlag" @click="selectTemporal" class="btn-check label-button" name="gbtnradio" id="temporalbtnradio3" value=2 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="temporalbtnradio3">Not Enough Information</label>
                                        </div>
                                        <p v-if="temporalFlag == null" class="text-center"> Please select a temporal label before moving on to temporal justification.</p>
                                        <div class="form-group text-right">
                                            <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button mt-2" :disabled="temporalFlag == null">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Next to temporal justification
                                                </span>
                                            </button>
                                        </div>
                                    </template>
                                    <template v-if="section == 1">
                                        <span class="badge text-bg-primary label-badge">Justification for Temporal Label</span>
                                        <p v-if="temporalFlag == 0">You have selected "Supports" for the temporal classification. Please use your mouse to select which temporal part of the evidence texts support the temporal parts of the claim.</p>
                                        <p v-if="temporalFlag == 1">You have selected "Refutes" for the temporal classification. Please use your mouse to select which temporal part of the evidence texts refutes the temporal parts of the claim.</p>
                                        <p v-if="temporalFlag == 2">You have selected "Not Enough Information" for the temporal classification. Please use your mouse to select which temporal part of the claim text was not able to be successfully annotated with the given evidences.</p>
                                        <ul v-if="temporalFlag != null" class="list-group list-group-horizontal temporal_justification mb-3 p-1">
                                            <template v-for="(item, index) in temporalJustification" :key="item">
                                                <li class="list-group-item temporal-item">
                                                    {{ item }}
                                                    <a href v-on:click.prevent="deleteTemporalJustification" :id="index"> <span class="badge bg-danger rounded-pill">
                                                            <font-awesome-icon icon="fa-solid fa-times" /></span></a>
                                                </li>
                                            </template>
                                        </ul>
                                        <div class="form-group text-center">
                                            <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2 mr-3">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Back to temporal label
                                                </span>
                                            </button>
                                            <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2" :disabled="temporalFlag == null || temporalJustification.length == 0">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Next to general label
                                                </span>
                                            </button>
                                        </div>
                                    </template>
                                    <template v-if="section == 2">
                                        <div class="form-group mb-1">
                                            <span class="badge text-bg-primary label-badge">General Facts Label</span>
                                        </div>
                                        <div class="btn-group w-100" role="group" aria-label="Basic radio toggle button group">
                                            <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio1" value=0 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="generalbtnradio1">Supports</label>

                                            <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio2" value=1 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="generalbtnradio2">Refutes</label>

                                            <input type="radio" v-model="generalFlag" @click="selectGeneral" class="btn-check label-button" name="tbtnradio" id="generalbtnradio3" value=2 autocomplete="off">
                                            <label class="btn btn-outline-primary label-button" for="generalbtnradio3">Not Enough Information</label>
                                        </div>
                                        <div class="form-group text-center">
                                            <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-3 mt-2 mr-3">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Back to temporal justification
                                                </span>
                                            </button>
                                            <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-3 mt-2" :disabled="generalFlag == null">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Next to general justification
                                                </span>
                                            </button>
                                        </div>
                                    </template>
                                    <template v-if="section == 3">
                                        <span class="badge text-bg-primary label-badge">Justification for General Label</span>
                                        <p v-if="generalFlag == 0">You have selected "Supports" for the general classification. Please use your mouse to select which general part of the evidence texts support the general parts of the claim.</p>
                                        <p v-if="generalFlag == 1">You have selected "Refutes" for the general classification. Please use your mouse to select which general part of the evidence texts refutes the general parts of the claim.</p>
                                        <p v-if="generalFlag == 2">You have selected "Not Enough Information" for the general classification. Please use your mouse to select which general part of the claim text was not able to be successfully annotated with the given evidences.</p>
                                        <ul v-if="generalFlag != null" class="list-group list-group-horizontal temporal_justification mb-3 p-1">
                                            <template v-for="(item, index) in generalJustification" :key="item">
                                                <li class="list-group-item temporal-item">
                                                    {{ item }}
                                                    <a href v-on:click.prevent="deleteGeneralJustification" :id="index"> <span class="badge bg-danger rounded-pill">
                                                            <font-awesome-icon icon="fa-solid fa-times" /></span></a>
                                                </li>
                                            </template>
                                        </ul>
                                        <div class="form-group text-center">
                                            <button @click="previousAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2 mr-3">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Back to general label
                                                </span>
                                            </button>
                                            <button @click="nextAnnotationProcess" type="submit" class="form-control btn btn-dark submit px-3 annotate-next-button-2 mt-2" :disabled="generalFlag == null || generalJustification.length == 0">
                                                <span class="badge text-bg-light ml-3 annotate-next">
                                                    Finish Annotation
                                                </span>
                                                <span v-if="count != 1" class="badge text-bg-light ml-3 move-on">
                                                    and move on to the next one
                                                </span>
                                                <span v-else class="badge text-bg-light ml-3 move-on">
                                                    no more claims to annotate
                                                </span>
                                            </button>
                                        </div>
                                    </template>
                                </div>
                            </div>
                            <div class="form-group d-md-flex">
                                <div class="w-100 text-md-right">
                                    <a href v-on:click.prevent="login = !login">Report a problem
                                        <font-awesome-icon icon="fa-solid fa-circle-arrow-right" /> </a>
                                </div>
                            </div>
                        </div>
                    </template>
                    <div v-if="count == 0" class="login-wrap p-4 p-lg-5 w-100">
                        <h2 class="">Sorry, there are no annotation claims left to do.</h2>
                    </div>
                    <div v-if="count == null" class="login-wrap p-4 p-lg-5 w-100">
                        <div class="spinner-border m-5" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <h2>Processing</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
</template>

<script>
import { STOPWORDS } from '../assets/js/stopwords.js';
import axios from "axios";
import { useUserStore } from "../stores/user";
import { useToast } from "vue-toastification";
const domain = "";
export default {
    setup() {
        // Get toast interface
        const toast = useToast();
        // Set up Pinia User store
        const store = useUserStore();
        const controller1 = new AbortController();
        const controller2 = new AbortController();
        return { store, toast, controller1, controller2 }
    },
    name: 'Home',
    data() {
        return {

            cancelTokenSource: null,
            source2: null,
            annotationTodo: "",
            evidenceCount: 0,
            currentEvidenceCount: 0,
            count: null,
            pendingAsync: false,

            temporalClaimElements: null,
            temporalEvidenceElements: null,
            relevantElements: null,
            topic: "",

            temporalFlag: null,
            generalFlag: null,

            temporalJustification: [],
            temporalJustificationEvidenceIds: [],
            generalJustification: [],
            generalJustificationEvidenceIds: [],

            // Indicates which step annotator is on, 0 - select temporal label, 1 - justify temporal label, 2 - select general label, 3 - justify general label
            section: 0,

        }
    },
    computed: {
        annotating_database() {
            return this.store.annotatingDatabase
        },
        annotator_email() {
            return this.store.annotatorEmail
        },
    },
    mounted() {
        // Check if key store values are set, otherwise redirect
        if (this.store.annotatorEmail == "" || this.store.annotatingDatabase == "" || this.store.isAuthenticatedAnnotation == false) {
            this.$router.push({ name: 'unauthorised' })
        }
    },
    created() {
        // Axios call to fetch first entry for annotation 
        const annotateData = {
            annotatorEmail: this.store.annotatorEmail,
            databaseId: this.store.annotatingDatabase,
        }
        axios
            .post(`${domain}/api/v1/database/annotation/get/`, annotateData)
            .then(response => {
                console.log(response.data.firstItem)
                this.annotationTodo = response.data.firstItem
                this.evidenceCount = this.annotationTodo.evidences.length
                console.log(response.data.count)
                this.count = response.data.count
                // If first evidence has no GPT labelling, need to get Django to fetch and update
                if (response.data.firstItem.evidences[0].claim_temporal == null || response.data.firstItem.evidences[0].evidence_temporal == null ||
                    response.data.firstItem.evidences[0].relevant_evidence == null || response.data.firstItem.evidences[0].topic == null) {
                    this.updateGPT(response.data.firstItem.evidences[0].id, true, true)
                } else {
                    this.temporalClaimElements = response.data.firstItem.evidences[0].claim_temporal
                    this.temporalEvidenceElements = response.data.firstItem.evidences[0].evidence_temporal
                    this.relevant_evidence = response.data.firstItem.evidences[0].relevant_evidence
                    this.topic = response.data.firstItem.evidences[0].topic
                    console.log(this.temporalClaimElements)
                    console.log(this.temporalEvidenceElements)
                    console.log(this.relevant_evidence)
                    console.log(this.topic)
                    this.$nextTick(() => {
                        this.highlightTemporalElements();
                    });
                }

            })
            .catch(error => {
                // Request was made and server responded unfavourably
                if (error.response) {
                    this.toast.error(error);
                }
                // Request was made but no response received
                else if (error.request) {
                    this.toast.error("Received no response from the server. Please try again.");
                }
                // Something else happened
                else {
                    console.log(error)
                    this.toast.error(error);
                    this.toast.error("Sorry, an unknown error occurred. Please try again.");
                }
            })
    },
    methods: {
        sanitizeText(text) {
            // Remove single and double quotes
            text = text.replace(/['"]+/g, '');
            
            // Remove extra whitespaces
            text = text.replace(/\s+/g, ' ').trim();

            return text.replace(/\s*([.,?!:;])/g, '$1');
        },
        highlightTemporalElements() {
            if (this.section == 0 || this.section == 1) {
                const claimText = this.$refs.temporalListner.textContent;
                const temporalElements = this.temporalClaimElements;
                const highlightedText = this.highlightText(claimText, temporalElements);

                // Replace the original text with the highlighted text
                this.$refs.temporalListner.innerHTML = highlightedText;

                const evidenceText = this.$refs.temporalEvidence.textContent;
                const temporalEvidenceElements = this.temporalEvidenceElements;
                const highlightedEvidenceText = this.highlightText(evidenceText, temporalEvidenceElements);

                // Replace the original text with the highlighted text
                this.$refs.temporalEvidence.innerHTML = highlightedEvidenceText;
            } else if (this.section == 2 || this.section == 3) {
                let claimText = this.$refs.temporalListner.textContent;
                claimText = claimText.replaceAll('<mark class="temporal-highlight">', '');
                claimText = claimText.replaceAll('</mark>', '');
                this.$refs.temporalListner.innerHTML = claimText;

                let evidenceText = this.$refs.temporalEvidence.textContent;
                evidenceText = evidenceText.replaceAll('<mark class="temporal-highlight">', '');
                evidenceText = evidenceText.replaceAll('</mark>', '');
                const relevantElements = this.relevant_evidence;
                // Loop through each relevant element and highlight it
                console.log("relevant")
                console.log(relevantElements)
                relevantElements.forEach(element => {
                    const words = element.split(' ');
                    let matchFound = true;
                    let i = 0;
                    while (matchFound && i < words.length) {
                        let word = words[i];
                        // remove parentheses
                        word = word.replace(/[()]/g, '');
                        if (!STOPWORDS.includes(word.toLowerCase())) { // check if the word is not a stopword
                            const regex = new RegExp('\\b(' + word + ')\\b', 'gi');
                            const matches = evidenceText.match(regex);
                            if (matches) {
                                matches.forEach(match => {
                                    const start = evidenceText.toLowerCase().indexOf(match.toLowerCase());
                                    const end = start + match.length;

                                    const span = document.createElement('span');
                                    span.classList.add('font-weight-bold');
                                    span.textContent = match;

                                    evidenceText = evidenceText.slice(0, start) + '<span class="font-weight-bold">' + evidenceText.slice(start, end) + '</span>' + evidenceText.slice(end);
                                });
                                i++;
                            } else {
                                matchFound = false;
                            }
                        } else {
                            i++;
                        }
                    }
                });
                this.$refs.temporalEvidence.innerHTML = evidenceText;


            }
        },
        highlightText(text, elements) {
            let highlightedText = text;

            elements.forEach(element => {
                const regex = new RegExp(element, 'g');
                highlightedText = highlightedText.replace(regex, `<mark class="temporal-highlight">$&</mark>`);
            });

            return highlightedText;
        },
        homepage() {
            if (this.cancelTokenSource) {
                this.cancelTokenSource.cancel('Openai update canceled by the user due to going back to homepage.');
            }
            this.$router.push({ name: 'homepage' })
        },
        updateGPT(evidence_id, newLoad, newClaim) {
            console.log(this.pendingAsync)
            this.cancelTokenSource = axios.CancelToken.source();
            // Cancel any pending openai update
            this.cancelTokenSource.cancel('Openai update canceled by the user due to submission of annotation.');
            if (newClaim || (this.pendingAsync == false && newLoad) || (this.pendingAsync == false && evidence_id != this.annotationTodo.evidences[this.currentEvidenceCount].id)) {
                this.pendingAsync = true;
                axios.put(`${domain}/api/v1/database/evidence/updateGPT/${evidence_id}/`, {cancelToken: this.cancelTokenSource.token})
                .then(response => {
                    // Do something with the response, e.g. update a local variable
                    if (evidence_id == this.annotationTodo.evidences[this.currentEvidenceCount].id) {
                        this.relevant_evidence = response.data.evidence_relevant;
                        this.temporalClaimElements = response.data.claim_temporal;
                        this.temporalEvidenceElements = response.data.evidence_temporal;
                        this.topic = response.data.topic;
                        this.$nextTick(() => {
                            this.highlightTemporalElements();  
                        });
                    }
                    this.pendingAsync = false;
                })
                .catch(error => {
                    if (axios.isCancel(error)) {
                        console.log('Fetching openai canceled duee to navigation:', error.message);
                    } else {    
                        // Handle any errors that occurred during the request
                        console.error(error);
                    }
                });
            } else if (this.pendingAsync == false && evidence_id == this.annotationTodo.evidences[this.currentEvidenceCount].id) {
                this.highlightTemporalElements();
            }
        },
        nextAnnotationProcess() {
            this.section = this.section + 1;
            if (this.section == 1 || this.section == 3) {
                this.updateGPT(this.annotationTodo.evidences[this.currentEvidenceCount].id, false, false);
                this.captureJustifications();
            } else {
                // Remove all event listeners
                this.updateGPT(this.annotationTodo.evidences[this.currentEvidenceCount].id, false, false);
                this.removeEventListeners();
            }
            if (this.section == 4) {
                this.nextAnnotate()
            }
        },
        previousAnnotationProcess() {
            this.section = this.section - 1;
            this.updateGPT(this.annotationTodo.evidences[this.currentEvidenceCount].id, false, false);
            if (this.section == 1 || this.section == 3) {
                this.captureJustifications();
            } else {
                // Remove all event listeners
                this.removeEventListeners();
            }
        },
        selectTemporal() {
            this.temporalJustification = [];
            this.temporalJustificationEvidenceIds = [];
        },
        selectGeneral() {
            this.generalJustification = [];
            this.generalJustificationEvidenceIds = [];
        },
        removeEventListeners() {
            document.removeEventListener('mouseup', this.eventListenerEvidence);
            document.removeEventListener('mouseup', this.generalEventListenerEvidence);
        },
        captureJustifications() {
            if (this.section == 1) {
                // Temporal justifications
                if (this.temporalFlag == 2) {
                    this.captureTemporalJustificationsNotEnoughInformation();
                } else {
                    this.captureTemporalJustificationsSupportsRefutes();
                }
            } else if (this.section == 3){
                // General justifications
                if (this.generalFlag == 2) {
                    this.captureGeneralJustificationsNotEnoughInformation();
                } else {
                    this.captureGeneralJustificationsSupportsRefutes();
                }
            }
        },
        captureTemporalJustificationsNotEnoughInformation() {
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            this.$refs.temporalListner.addEventListener('mouseup', this.eventListener)
        },
        captureTemporalJustificationsSupportsRefutes() {
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            document.addEventListener('mouseup', this.eventListenerEvidence)
        },
        captureGeneralJustificationsNotEnoughInformation() {
            document.removeEventListener('mouseup', this.generalEventListenerEvidence)
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            this.$refs.temporalListner.addEventListener('mouseup', this.generalEventListener)
        },
        captureGeneralJustificationsSupportsRefutes() {
            this.$refs.temporalListner.removeEventListener('mouseup', this.generalEventListener)
            this.$refs.temporalListner.removeEventListener('mouseup', this.eventListener)
            document.removeEventListener('mouseup', this.eventListenerEvidence)
            document.addEventListener('mouseup', this.generalEventListenerEvidence)
        },
        addTemporalJustification(e) {
            if (window.getSelection().toString().trim() != "") {
                // Prevent duplicate justification text from being added
                if (!this.temporalJustification.includes(window.getSelection().toString().trim())) {
                    this.temporalJustification.push(window.getSelection().toString().trim());
                    console.log(this.temporalJustification);

                    // Do not want to add evidence ids if it is adding claim details
                    if (this.temporalFlag != 2) {
                        let evidenceId = parseInt(e.target.id);

                        if (e.target.nodeName.toLowerCase() === 'mark') {
                            // If the target element is a <mark> element, find the nearest parent element with an id attribute
                            let parentWithId = e.target.closest('[id]');
                            if (parentWithId) {
                                evidenceId = parseInt(parentWithId.id);
                            }
                        }

                        this.temporalJustificationEvidenceIds.push(evidenceId);
                    }
                    console.log(this.temporalJustificationEvidenceIds);
                }
            }
        },
        addGeneralJustification(e) {
            if (window.getSelection().toString().trim() != "") {
                if (!this.generalJustification.includes(window.getSelection().toString().trim())) {
                    // Prevent duplicate justification text from being added
                    this.generalJustification.push(window.getSelection().toString().trim());
                    console.log(this.generalJustification);
                    if (this.generalFlag != 2) {
                        let evidenceId = parseInt(e.target.id);

                        if (e.target.nodeName.toLowerCase() === 'span') {
                            let parentWithId = e.target.closest('[id]');
                            if (parentWithId) {
                                evidenceId = parseInt(parentWithId.id);
                            }
                        }

                        this.generalJustificationEvidenceIds.push(evidenceId);
                    }
                    console.log(this.generalJustificationEvidenceIds);
                }
            }
        },
        generalEventListener: function (event) {
            this.addGeneralJustification(event);
        },
        generalEventListenerEvidence: function (event) {
            let target = event.target;
            while (target && !target.classList.contains('evidence-text')) {
                if (target.parentElement) {
                    target = target.parentElement;
                } else {
                    break;
                }
            }

            if (target && target.classList.contains('evidence-text')) {
                this.addGeneralJustification(event);
            }
        },
        eventListener: function (event) {
            this.addTemporalJustification(event);
        },
        eventListenerEvidence: function (event) {
            let target = event.target;
            while (target && !target.classList.contains('evidence-text')) {
                if (target.parentElement) {
                    target = target.parentElement;
                } else {
                    break;
                }
            }

            if (target && target.classList.contains('evidence-text')) {
                this.addTemporalJustification(event);
            }
        },
        deleteTemporalJustification: function (e) {
            const id = e.currentTarget.id;
            this.temporalJustification.splice(id, 1);
            // Do not delete from ids if it was a claim removal
            if (this.temporalFlag != 2) {
                this.temporalJustificationEvidenceIds.splice(id, 1);
            }
        },
        deleteGeneralJustification: function (e) {
            const id = e.currentTarget.id;
            this.generalJustification.splice(id, 1);
            // Do not delete from ids if it was as claim removal
            if (this.generalFlag != 2) {
                this.generalJustificationEvidenceIds.splice(id, 1);
            }
        },
        processFlags(flag) {
            if (flag == 0) {
                return "SUPPORTS"
            } else if (flag == 1) {
                return "REFUTES"
            } else {
                return "NOT ENOUGH INFORMATION"
            }
        },
        processOverallFlag(temporal, general) {
            // Flags can only be 0, 1 or 2
            // If either one refutes, return refute
            if (temporal == 1 || general == 1) {
                return "REFUTES"
                // If either one is not enough info, return not enough info
            } else if (temporal == 2 || general == 2) {
                return "NOT ENOUGH INFORMATION"
            } else {
                return "SUPPORTS"
            }
        },
        submitAnnotation() {
            // Submit annotation then add justification in
            var submittedAnnotateData;
            submittedAnnotateData = {
                claimId: this.annotationTodo.id,
                evidenceId: this.annotationTodo.evidences[this.currentEvidenceCount].id,
                email: this.store.annotatorEmail,
                temporal_flag: this.processFlags(this.temporalFlag),
                general_flag: this.processFlags(this.generalFlag),
                overall_flag: this.processOverallFlag(this.temporalFlag, this.generalFlag)
            }
            axios
                .post(`${domain}/api/v1/database/annotation/add/`, submittedAnnotateData)
                .then(initialresponse => {
                    console.log(initialresponse.data)
                    // Add justification after annotation successfully added
                    for (var i = 0; i < this.temporalJustification.length; i++) {
                        const justificationText = this.temporalJustification[i]
                        var submittedJustificationData;
                        // For claim justificaion, no need add evidence ids
                        if (this.temporalFlag == 2) {
                            submittedJustificationData = {
                                annotation: initialresponse.data.id,
                                temporal: true,
                                claimPart: true,
                                justification: justificationText
                            }
                        } else {
                            submittedJustificationData = {
                                annotation: initialresponse.data.id,
                                evidence: this.temporalJustificationEvidenceIds[i],
                                temporal: true,
                                claimPart: false,
                                justification: justificationText
                            }
                        }
                        console.log("justification")
                        console.log(submittedJustificationData)

                        axios.post(`${domain}/api/v1/database/annotation/add/justification/`, submittedJustificationData).then(response => {
                            console.log(response.data)
                        }).catch(error => {
                            console.log(error)
                            // Request was made and server responded unfavourably
                            if (error.response.data.non_field_errors[0]) {
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

                    }

                    for (var i = 0; i < this.generalJustification.length; i++) {
                        const justificationText = this.generalJustification[i]
                        var submittedJustificationData;
                        // For claim justificaion, no need add evidence ids
                        if (this.generalFlag == 2) {
                            submittedJustificationData = {
                                annotation: initialresponse.data.id,
                                temporal: false,
                                claimPart: true,
                                justification: justificationText
                            }
                        } else {
                            submittedJustificationData = {
                                annotation: initialresponse.data.id,
                                evidence: this.generalJustificationEvidenceIds[i],
                                temporal: false,
                                claimPart: false,
                                justification: justificationText
                            }
                        }
                        axios.post(`${domain}/api/v1/database/annotation/add/justification/`, submittedJustificationData).then(response => {
                            console.log(response.data)
                        }).catch(error => {
                            console.log(error.data)
                            // Request was made and server responded unfavourably
                            if (error.response.data.non_field_errors[0]) {
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
                    }
                    // Resets the GPT Data
                    this.currentEvidenceCount = this.currentEvidenceCount + 1;
                    this.temporalClaimElements = null;
                    this.temporalEvidenceElements = null;
                    this.relevant_evidence = null;
                    this.topic = "";
                    if (this.currentEvidenceCount == this.evidenceCount) {
                        // Axios call to fetch first entry for annotation 
                        // Only fetch next entry when all evidences annotated
                        const annotateData = {
                            annotatorEmail: this.store.annotatorEmail,
                            databaseId: this.store.annotatingDatabase,
                        }
                        axios
                            .post(`${domain}/api/v1/database/annotation/get/`, annotateData)
                            .then(response => {
                                console.log("data")
                                console.log(response.data)
                                this.annotationTodo = response.data.firstItem
                                this.count = response.data.count
                                this.section = 0;
                                this.currentEvidenceCount = 0;
                                this.evidenceCount = this.annotationTodo.evidences.length
                                // Clears out previous entries
                                this.selectTemporal();
                                this.selectGeneral();
                                this.temporalFlag = null;
                                this.generalFlag = null;
                                if (response.data.firstItem.evidences[0].claim_temporal == null || response.data.firstItem.evidences[0].evidence_temporal == null ||
                                    response.data.firstItem.evidences[0].relevant_evidence == null || response.data.firstItem.evidences[0].topic == null) {
                                    this.updateGPT(response.data.firstItem.evidences[0].id, false, true)
                                } else {
                                    this.temporalClaimElements = response.data.firstItem.evidences[0].claim_temporal
                                    this.temporalEvidenceElements = response.data.firstItem.evidences[0].evidence_temporal
                                    this.relevant_evidence = response.data.firstItem.evidences[0].relevant_evidence
                                    this.topic = response.data.firstItem.evidences[0].topic
                                    this.$nextTick(() => {
                                        this.highlightTemporalElements();
                                    });
                                }
                            })
                            .catch(error => {
                                // Request was made and server responded unfavourably
                                if (error.response.data.non_field_errors[0]) {
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
                    } else {
                        this.section = 0;
                        this.selectTemporal();
                        this.selectGeneral();
                        this.temporalFlag = null;
                        this.generalFlag = null;
                        if (this.annotationTodo.evidences[this.currentEvidenceCount].claim_temporal == null || this.annotationTodo.evidences[this.currentEvidenceCount].evidence_temporal == null ||
                            this.annotationTodo.evidences[this.currentEvidenceCount].relevant_evidence == null || this.annotationTodo.evidences[this.currentEvidenceCount].topic == null) {
                            this.updateGPT(this.annotationTodo.evidences[this.currentEvidenceCount].id, true, true)
                        } else {
                            this.temporalClaimElements = this.annotationTodo.evidences[this.currentEvidenceCount].claim_temporal
                            this.temporalEvidenceElements = this.annotationTodo.evidences[this.currentEvidenceCount].evidence_temporal
                            this.relevant_evidence = this.annotationTodo.evidences[this.currentEvidenceCount].relevant_evidence
                            this.topic = this.annotationTodo.evidences[this.currentEvidenceCount].topic
                            this.$nextTick(() => {
                                this.highlightTemporalElements();
                            });
                        }
                    }

                })
                .catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    if (error.response.data.non_field_errors[0]) {
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
        nextAnnotate() {
            // If last claim already, we simply submit the annotation
            if (this.count == 1 && this.currentEvidenceCount == this.evidenceCount) {
                this.submitAnnotation();
                this.count = 0;
                return
            }
            // Otherwise we submit the annotation and fetch the next claim
            this.submitAnnotation();
        },
    },
}
</script>

<style scoped>
.annotator {
    background-color: #f4f4f4;
    border-radius: 5px;
}

#annotating-label {
    font-size: 23px;
    font-weight: 700;
}

.move-on {
    font-size: 13px;
}

.submit {
    font-size: 18px;
    font-weight: 500;
    width: 380px;
    height: 70px;
}

.topic-badge {
    font-size: 16px;
    background-color:#000000;
    padding:10px;
}

.claim-badge {
    font-size: 16px;
    margin-bottom: 5px;
}

.claim-text {
    font-weight: 800;
}

.evidence-div {
    background-color: #f4f4f4;
    border: 1px solid #e1e0e0;
}

.label-badge {
    font-size: 18px;
    margin-bottom: 10px;
}

.label-button {
    font-size: 16px;
    font-weight: 800;
}

.annotation {
    border: 1px solid #e1e0e0;
}

.temporal_justification {
    width: 100%;
    height: 65px;
    background-color: #f4f4f4;
    border: 1px solid #e1e0e0;
    white-space: nowrap;
    overflow-x: auto;
}

.temporal-item {
    margin-left: 5px;
}

.annotate-next {
    font-size: 17px;
}

.annotate-next-button {
    width: 285px;
    height: 50px;
}

.annotate-next-button-2 {
    width: 255px;
    height: 65px;
}

.annotate-next-button-3 {
    width: 300px;
    height: 50px;
}

.home-button {
    width: 180px;
    height: 46px;
    font-size: 30px;
}

.temporal-highlight {
    background-color: yellow;
    pointer-events: none!important;
}

.font-weight-bold {
    font-weight: 1000;
}

.yellow-highlight {
    background-color: yellow;
    display: inline-block;
    width: 100px;
    height: 2em;
    line-height: 1em;
    vertical-align: middle;
}
</style>
