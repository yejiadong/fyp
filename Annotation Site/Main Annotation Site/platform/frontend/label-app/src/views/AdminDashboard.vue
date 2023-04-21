<template>
<section class="ftco-section">
    <div class="container add">
        <div class="row top-bar">
            <div class="col-md-9 mb-8">
                <h1 class="heading-section">Welcome {{ store.email }}!</h1>
                <p>Institution: {{ store.institution }}</p>
            </div>
            <div class="col-md-3 mb-2">
                <button @click="logout" type="submit" class="form-control btn btn-dark submit px-3 logout-button mt-3">
                    Logout
                </button>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-12">
                <div class="wrap d-md-flex">
                    <div class="login-wrap p-4 p-lg-5 col-md-12 col-lg-12">
                        <div class="d-flex">
                            <div class="w-100">
                                <h4 class="mb-4">Databases</h4>
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-12 col-lg-12">
                                <div class="wrap p-1 p-lg-1">
                                    <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link active" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Add Database</button>
                                        </li>
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">Add Claims</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="wrap d-md-flex">
                                            <div class="text-wrap p-4 p-lg-5 text-center d-flex order-md-last">
                                                <div class="text w-100">
                                                    <div class="text w-100 list-database overflow-auto">
                                                        <h4 class="view-database-label">Databases</h4>
                                                        <ol class="list-group list-group-numbered">
                                                            <transition-group name="listtransition">
                                                                <template v-for="item in returnData" :key="item.id">
                                                                    <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                        <div class="ms-2 me-auto w-80">
                                                                            <div class="fw-bold">{{ item.name }}</div>
                                                                            {{ item.description }}
                                                                            <div>
                                                                                <span class="numberClaims">{{ item.num_claims }} claims</span>
                                                                            </div>
                                                                            <div class="fw-bold">
                                                                                <span v-if="item.is_active == true" class="badge bg-primary rounded-pill">Active</span>
                                                                                <span v-else="item.is_active == false" class="badge bg-primary rounded-pill">Not Active</span>
                                                                            </div>
                                                                        </div>
                                                                        <div class="options w-40">
                                                                            <button v-if="item.is_active == false" class="btn btn-success delete-button" value=True @click="activateDatabase" :id="'activate-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Activate
                                                                            </button>
                                                                            <button v-else="item.is_active == true" class="btn btn-danger delete-button" value=False @click="activateDatabase" :id="'activate-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Deactivate
                                                                            </button>
                                                                            <button class="btn btn-primary delete-button" @click="deleteDatabase" :id="'delete-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Delete
                                                                            </button>
                                                                        </div>
                                                                    </li>
                                                                </template>
                                                            </transition-group>
                                                        </ol>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="login-wrap p-4 p-lg-5">
                                                <form @submit.prevent="mainAddDatabase" class="add-database-form">
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="name">Name of database</label>
                                                        <input type="text" v-model="databaseName" class="form-control" placeholder="Database Name" required>
                                                    </div>
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="name">Short Description</label>
                                                        <input type="text" v-model="description" class="form-control" placeholder="Write a short description." required>
                                                    </div>
                                                    <div class="form-group mb-3">
                                                        <label class="label" for="password">Database Password</label>
                                                        <input type="password" v-model="databasePassword" class="form-control" placeholder="Password" :maxlength="20" required>
                                                        <div class="password_validation" v-text="(20 - databasePassword.length) + ' chars left'"></div>
                                                    </div>
                                                    <div class="form-group mb-3 upload">
                                                        <label class="label" for="password">Upload Claims and Evidences</label>
                                                        <file-pond name="uploadFile" ref="pond" class="upload-file" class-name="upload-file" credits="false" label-idle="Drop files here..." allow-multiple="true" required="true" maxFiles=3 accepted-file-types="application/json" v-bind:files="uploadedFiles" v-on:init="handleFilePondInit" />
                                                    </div>
                                                    <div class="form-group">
                                                        <button type="submit" class="form-control btn btn-primary submit px-3">Add Database</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="wrap d-md-flex">
                                            <div class="text-wrap p-4 p-lg-5 text-center d-flex order-md-last">
                                                <div class="text w-100">
                                                    <div class="text w-100 list-database overflow-auto">
                                                        <h4 class="view-database-label">Claims</h4>
                                                        <ol class="list-group list-group-numbered">
                                                            <transition-group name="listtransition">
                                                                <template v-for="item in claimData" :key="item.id">
                                                                    <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                        <div class="ms-2 me-auto w-80">
                                                                            <div class="fw-bold">{{ item.content }}</div>
                                                                        </div>
                                                                        <div class="options w-40">
                                                                            <button class="btn btn-primary delete-button" @click="deleteClaim" :id="'delete-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                Delete
                                                                            </button>
                                                                        </div>
                                                                    </li>
                                                                </template>
                                                            </transition-group>
                                                        </ol>
                                                    </div>
                                                </div>
                                            </div>
                                            <!-- Add Evidence Modal -->
                                            <div class="modal fade" id="evidenceModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Add evidence</h1>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <form @submit.prevent="addEvidenceConfirm" class="add-evidence-form">
                                                            <div class="modal-body">
                                                                <div class="form-group mb-3">
                                                                    <label class="label" for="password">Evidence Content</label>
                                                                    <input type="text" ref="evidenceField" class="form-control" placeholder="Evidence Content" required>
                                                                </div>
                                                            </div>
                                                            <div class="modal-footer">
                                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                                <button class="btn btn-primary addEvidenceButton" data-bs-dismiss="modal">Add evidence</button>
                                                            </div>
                                                        </form>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="login-wrap p-4 p-lg-5">
                                                <form @submit.prevent="addClaimAndEvidenceManual">
                                                    <div class="form-group">
                                                        <label class="label" for="name">Select a database</label>
                                                        <div class="databaseDropdown">
                                                            <button class="btn btn-secondary dropdown-toggle" type="button" ref="selectDatabaseBtn" data-bs-toggle="dropdown" aria-expanded="false">
                                                                Select a Database
                                                            </button>
                                                            <ul class="dropdown-menu" aria-labelledby="selectDatabase">
                                                                <template v-for="item in returnData" :key="item.id">
                                                                    <li value="item.id">
                                                                        <a class="dropdown-item" v-on:click="changeSelectedDatabase(item.id, item.name)">{{ item.id }} - {{ item.name }}</a>
                                                                    </li>
                                                                </template>
                                                            </ul>
                                                        </div>
                                                    </div>
                                                    <div class="form-check form-switch form-switch-lg">
                                                        <input class="form-check-input addClaimsViaUpload" type="checkbox" v-model="uploadFiles" role="switch" id="flexSwitchCheckDefault">
                                                        <label class="form-check-label" for="flexSwitchCheckDefault">Check to upload files instead</label>
                                                    </div>
                                                    <template v-if="!uploadFiles">
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="name">Claim</label>
                                                            <input type="text" v-model="addClaimContent" class="form-control" placeholder="Claim content." required>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Original ID</label>
                                                            <input type="number" v-model="addClaimOriginalID" class="form-control" placeholder="Original ID" required>
                                                        </div>
                                                        <div class="form-group mb-3">
                                                            <label class="label" for="password">Add Evidence</label>
                                                            <button class="btn btn-secondary px-3 ml-4" data-bs-toggle="modal" data-bs-target="#evidenceModal">Add Evidence</button>
                                                            <div v-if="addEvidenceStore.length != 0" class="evidences overflow-auto">
                                                                <ol class="list-group list-group-numbered">
                                                                    <template v-for="(evidence, index) in addEvidenceStore" :key="index">
                                                                        <li class="list-group-item d-flex justify-content-between align-items-start  mt-2">
                                                                            <div class="ms-2 me-auto w-80">
                                                                                {{ evidence }}
                                                                            </div>
                                                                            <div class="options w-40">
                                                                                <button @click="deleteEvidenceConfirm" class="btn btn-primary delete-button px-1" :id="'delete-' + index" style="--bs-btn-font-size: 0.9rem;" type="button">
                                                                                    Remove Evidence
                                                                                </button>
                                                                            </div>
                                                                        </li>
                                                                    </template>
                                                                </ol>
                                                            </div>
                                                            <div v-else class="mt-2">
                                                                <p>No evidence added yet.</p>
                                                            </div>
                                                        </div>
                                                    </template>
                                                    <template v-else="!uploadFiles">
                                                        <div class="form-group mb-3 upload">
                                                            <label class="label" for="password">Upload Claims and Evidences</label>
                                                            <file-pond name="uploadFilesManual" ref="manualpond" class="upload-file" class-name="upload-file" credits="false" label-idle="Drop files here..." allow-multiple="true" required="true" maxFiles=3 accepted-file-types="application/json" v-bind:files="uploadedFilesManual" v-on:init="handleFilePondInit" />
                                                        </div>
                                                    </template>
                                                    <div class="form-group">
                                                        <button class="form-control btn btn-primary submit px-3">Add Claims</button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tab-pane fade" id="pills-contact" role="tabpanel" aria-labelledby="pills-contact-tab">1</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-12">
                <div class="wrap d-md-flex">
                    <div class="login-wrap p-4 p-lg-5 col-md-12 col-lg-12">
                        <div class="d-flex">
                            <div class="w-100">
                                <h4 class="mb-4">Annotation</h4>
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-12 col-lg-12">
                                <div class="wrap p-1 p-lg-1">
                                    <ul class="nav nav-pills mb-3" id="pills-tab-annotation" role="tablist">
                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link active" id="pills-annotation-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">Generate Annotation Results</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="tab-content" id="pills-tabContent">
                            <div class="tab-pane fade show active" id="pills-annotation" role="tabpanel" aria-labelledby="pills-annotation-tab">
                                <div class="row justify-content-center">
                                    <div class="col-md-12 col-lg-12">
                                        <div class="col-md-12 col-lg-12 login-wrap p-4 p-lg-5">
                                            <div class="form-group">
                                                <label class="label" for="name">Select a database</label>
                                                <div class="databaseDropdown">
                                                    <button class="btn btn-secondary dropdown-toggle" type="button" ref="selectDatabaseBtnAnnotation" data-bs-toggle="dropdown" aria-expanded="false">
                                                        Select a Database
                                                    </button>
                                                    <ul class="dropdown-menu" aria-labelledby="selectDatabase">
                                                        <template v-for="item in returnData" :key="item.id">
                                                            <li value="item.id">
                                                                <a class="dropdown-item" v-on:click="changeSelectedDatabaseAnnotation(item.id, item.name)">{{ item.id }} - {{ item.name }}</a>
                                                            </li>
                                                        </template>
                                                    </ul>
                                                </div>
                                                <div v-if="!this.processing && this.currentAnnotation && this.currentAnnotation != '' && this.selectedDatabaseAnnotation && this.selectedDatabaseAnnotation != ''" class="container">
                                                    <div class="row justify-content-center">
                                                        <div class="col-md-12 col-lg-12 login-wrap p-4 p-lg-5">
                                                            <div class="d-flex">
                                                                <div class="w-100">
                                                                    <span class="badge text-light topic-badge mb-3">Topic: {{ this.currentAnnotation.evidence.topic }}</span> <br />
                                                                    <span class="badge text-bg-primary claim-badge ml-1 mb-3">Claim</span>
                                                                    <h3 class="mb-4 claim-text ml-1" ref="temporalListner">{{ this.currentAnnotation.claim.content }}</h3>
                                                                </div>
                                                            </div>
                                                            <div class="form-group mb-3 evidence-div p-2">
                                                                <div class="d-flex">
                                                                    <div class="w-100">
                                                                        <h5 class="mb-2 evidence-text" ref="temporalEvidence">{{ this.currentAnnotation.evidence.content }}</h5>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row justify-content-center annotation">
                                                        <div class="col-md-6 col-lg-6 p-2 p-lg-4 left-annotation">
                                                            <div class="text w-100 overflow-auto">
                                                                <div class="d-flex w-100">
                                                                    <h4 class="gpt_label mb-3">Annotation Done:</h4>
                                                                </div>
                                                                <div class="annotation-stats mt-2 p-2 pt-3">
                                                                    <div class="stat-circle supports">
                                                                        <i class="fas fa-check"></i>
                                                                        <span class="annotation_numbers">{{ this.currentAnnotation.evidence.label_counts['SUPPORTS'] ? this.currentAnnotation.evidence.label_counts['SUPPORTS'] : 0 }}</span>
                                                                    </div>
                                                                    <div class="stat-circle refutes">
                                                                        <i class="fas fa-times"></i>
                                                                        <span class="annotation_numbers">{{ this.currentAnnotation.evidence.label_counts['REFUTES'] ? this.currentAnnotation.evidence.label_counts['REFUTES'] : 0 }}</span>
                                                                    </div>
                                                                    <div class="stat-circle not-enough-info">
                                                                        <i class="fas fa-question"></i>
                                                                        <span class="annotation_numbers">{{ this.currentAnnotation.evidence.label_counts['NOT ENOUGH INFO'] ? this.currentAnnotation.evidence.label_counts['NOT ENOUGH INFO'] : 0 }}</span>
                                                                    </div>
                                                                </div>
                                                                <div class="annotation-stats mb-3 pt-1 pl-2 p-2 pb-3">
                                                                    <span class="label-text"> Supports </span>
                                                                    <span class="label-text ml-4"> Refutes </span>
                                                                    <span class="label-text ml-1"> Not enough info</span>
                                                                </div>
                                                                <!-- Submit Final Label Modal -->
                                                                <div class="modal fade" ref="finalModal" id="finalModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                                    <div class="modal-dialog">
                                                                        <div class="modal-content">
                                                                            <div class="modal-header">
                                                                                <h1 class="modal-title fs-5" id="exampleModalLabel">Successfully submited final label!</h1>
                                                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                                            </div>
                                                                            <div class="modal-body">
                                                                                <template v-if="(this.paraphrases == null || this.paraphrases.length != 5) && (this.paraphraseFlag != false)">
                                                                                    <div class="spinner-grow text-secondary" role="status">
                                                                                        <span class="visually-hidden">Loading...</span>
                                                                                    </div>
                                                                                    <span> Loading paraphrases ... Please be patient.</span>
                                                                                </template>
                                                                                <template v-else-if="this.paraphraseFlag == false">
                                                                                    <h5> Claim: </h5>
                                                                                    <p><strong>{{ this.currentAnnotation.claim.content }} </strong></p>
                                                                                    <hr />
                                                                                    <h6> Here are the paraphrases added / retrieved: </h6>
                                                                                    <p class="mt-2" v-for="item in this.paraphrases">{{ item }}</p>
                                                                                </template>
                                                                                <template v-else>
                                                                                    <h6>No paraphrases are added. </h6>
                                                                                </template>
                                                                            </div>
                                                                            <div class="modal-footer">
                                                                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <ol class="list-group list-group-numbered">
                                                                    <transition-group name="listtransition">
                                                                        <template v-for="item in this.currentAnnotation.annotations" :key="item.id">
                                                                            <li class="list-group-item d-flex justify-content-between align-items-start">
                                                                                <div class="ms-2 me-auto w-100">
                                                                                    <div class="fw-bold">{{ item.annotator_email }} </div>
                                                                                    {{ formatDate(item.annotated_at) }}
                                                                                    <div>
                                                                                        <span class="numberClaims">General Label: {{ item.general_label }} </span>
                                                                                        <br /><span class="numberClaims">Temporal Label: {{ item.temporal_label }} </span>
                                                                                    </div>
                                                                                    <div class="fw-bold">
                                                                                        <span class="numberClaims">Final Label: <strong>{{ item.overall_label }}</strong> </span>
                                                                                    </div>
                                                                                    <button class="btn btn-success ignore" value=True @click="ignoreAnnotation($event, item.overall_label)" :id="'deleteOne-' + item.id" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                        Ignore this annotation
                                                                                    </button>
                                                                                    <button class="btn btn-danger ignore ml-2" value=False @click="ignoreAnnotator($event, item.id, item.overall_label)" :id="'deleteAll-' + item.annotator_email" style="--bs-btn-font-size: 1rem;" type="button">
                                                                                        Ignore all
                                                                                    </button>
                                                                                </div>
                                                                            </li>
                                                                        </template>
                                                                    </transition-group>
                                                                </ol>
                                                            </div>
                                                        </div>
                                                        <div class="col-md-5 col-lg-5 p-2 p-lg-4 gpt ml-3">
                                                            <div class="d-flex w-100">
                                                                <h6 class="gpt_label"> GPT's Predictions</h6>
                                                            </div>
                                                            <div class="d-flex">
                                                                <div class="w-100">
                                                                    <h5 class="mb-4 claim-text">General Label: {{ this.currentAnnotation.evidence.general_facts_label }}</h5>
                                                                    <p>{{ this.currentAnnotation.evidence.general_facts_justification }}</p>
                                                                </div>
                                                            </div>
                                                            <div class="d-flex">
                                                                <div class="w-100">
                                                                    <h5 class="mb-4 claim-text">Temporal Label: {{ this.currentAnnotation.evidence.time_label }}</h5>
                                                                    <p>{{ this.currentAnnotation.evidence.time_justification }}</p>
                                                                </div>
                                                            </div>
                                                            <div class="d-flex">
                                                                <div class="w-100">
                                                                    <h5 class="mb-4 claim-text">Final Model Label: {{ this.currentAnnotation.evidence.model_label.toUpperCase() }}</h5>
                                                                </div>
                                                            </div>
                                                            <div class="d-flex w-100">
                                                                <h6 class="gpt_label"> Submit Final Label</h6>
                                                            </div>
                                                            <div class="d-flex w-100">
                                                                <select v-model="selectedLabel" class="final-select">
                                                                    <option disabled value="">Select a final label</option>
                                                                    <option v-for="label in labels" :key="label.value" :value="label.value">
                                                                        {{ label.text }}
                                                                    </option>
                                                                </select>
                                                                <button @click="updateFinal" v-if="selectedLabel" class="submit-final" data-bs-toggle="modal" data-bs-target="#finalModal">
                                                                    <i class="bi bi-arrow-right-circle-fill submit-final-icon"></i>
                                                                </button>
                                                            </div>
                                                        </div>
                                                        <div class="row">
                                                            <div class="col-md-7 col-lg-7 p-2 p-lg-4"></div>
                                                            <div class="col-md-5 col-lg-5 p-2 p-lg-4 move-on">
                                                                <div class="d-flex w-100">
                                                                    <button @click="getFirstReviewableAnnotation" class="getNext" :disabled="!submitted">
                                                                        Next Review
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div v-else-if="this.processing">
                                                    <div class="spinner-grow text-secondary mt-4" role="status">
                                                        <span class="visually-hidden">Loading...</span>
                                                    </div>
                                                    <h4 class="p-2 mt-3 mb-3">Please wait while we check for more annotations to review. </h4> 
                                                </div>
                                                <div v-else-if="this.selectedDatabaseAnnotation == ''">
                                                    <h4 class="p-2 mt-3 mb-3">Select a database to view annotations to review. </h4> 
                                                </div>
                                                <div v-else>
                                                    <h4 class="p-2 mt-3 mb-3">There are no more claim evidence pairs to review for now. </h4> 
                                                </div>
                                            <div class="form-group mt-3" v-if="selectedDatabaseAnnotation">
                                                <button type="submit" @click=downloadJson class="form-control btn btn-primary submit px-3">Download Final Labels</button>
                                                <button type="submit" @click=getAnnotations class="form-control btn btn-primary submit px-3">Download Full Annotation Results</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
</section>
<template v-if="showModal">
    <div class="modal show" id="dashboardModal" style="display: block;">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" v-if="loadingAdd" id="dashboardModalLabel">Loading</h1>
                    <h1 class="modal-title fs-5" v-else id="dashboardModalLabel">Operation Completed</h1>
                    <button type="button" class="btn-close" v-if="loadingAdd == false" @click=clearModalMessage></button>
                </div>
                <div class="modal-body">
                    <h4></h4>
                    <div class="text w-100 list-database overflow-auto model-message">
                        <h6><strong>{{ claimNumber }}</strong> claims added in total.</h6>
                        <h6><strong>{{ evidenceNumber }}</strong> evidences added in total.</h6>
                        <template v-if="loadingAdd">
                            <div class="spinner-grow text-secondary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <span> Adding claims ... Please be patient.</span>
                        </template>
                        <ol class="list-group list-group-numbered" id="modelMessage">
                            <hr />
                            <h6><strong>Log: </strong></h6>
                            <template v-for="item in modalMessages">
                                <li class="message-list d-flex">
                                    <p>{{ item }}</p>
                                </li>
                            </template>
                        </ol>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" @click=clearModalMessage v-if="loadingAdd" class="btn btn-secondary" disabled>Close</button>
                    <button type="button" @click=clearModalMessage v-else class="btn btn-secondary">Close</button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal-backdrop show"></div>
</template>
</template>

<script>
import axios from "axios";
import { useUserStore } from "../stores/user";
import { useVuelidate } from '@vuelidate/core';
import { useToast } from "vue-toastification";
import { saveAs } from 'file-saver';
// Import FilePond
import vueFilePond from 'vue-filepond';
// Import plugins
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js';
// Import styles
import 'filepond/dist/filepond.min.css';
import { thisExpression } from "@babel/types";
// Create FilePond component
const FilePond = vueFilePond(FilePondPluginFileValidateType);
const domain = "";
export default {
    setup() {
        // Get toast interface
        const toast = useToast();
        // Set up Pinia User store
        const store = useUserStore();
        const token = store.token;
        if (token) {
            axios.defaults.headers.common['Authorization'] = "Token " + token
        } else {
            axios.defaults.headers.common['Authorization'] = ""
        }
        return { store, toast, v$: useVuelidate(), }
    },
    mounted() {
        this.getDatabases();
    },
    name: 'AdminDashboard',
    data() {
        return {

            uploadedFiles: [],
            databaseName: "",
            description: "",
            databasePassword: "",
            returnData: null,
            claimData: null,

            loadingAdd: false,
            fileReadObject: null,

            selectedDatabase: "",
            modeForClaims: "",

            uploadFiles: false,
            addClaimContent: "",
            addClaimOriginalID: "",

            uploadedFilesManual: [],
            addEvidenceStore: [],

            modalMessages: [],
            claimNumber: 0,
            evidenceNumber: 0,
            showModal: false,

            selectedDatabaseAnnotation: "",
            currentAnnotation: "",
            processing: false,

            selectedLabel: '',
            labels: [
                { text: 'Supports', value: 'Supports' },
                { text: 'Refutes', value: 'Refutes' },
                { text: 'Not Enough Information', value: 'Not Enough Info' },
            ],
            submitted: false,
            paraphrases: [],
            paraphraseFlag: true,

        };
    },
    computed: {
        kappaLabel() {
            if (this.kappa < 0) {
            return 'No agreement';
            } else if (this.kappa < 0.2) {
            return 'Poor agreement';
            } else if (this.kappa < 0.4) {
            return 'Fair agreement';
            } else if (this.kappa < 0.6) {
            return 'Moderate agreement';
            } else if (this.kappa < 0.8) {
            return 'Substantial agreement';
            } else if (this.kappa == "N/A"){
            return 'Unable to calculate Kappa (Perhaps not enough annotators)';
            } else {
            return 'Almost perfect agreement';
            }
        }
    },
    methods: {
        formatDate(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleString();
        },
        logout() {
            const store = useUserStore();
            store.removeToken()
            this.$router.push('/')
        },
        // Generates a random salt for database password
        generateRandomSalt() {
            let result = ' ';
            for (let i = 0; i < length; i++) {
                result += characters.charAt(Math.floor(Math.random() * 20));
            }
            return result;
        },
        reshuffle: function shuffle(array) {
            let currentIndex = array.length,
                randomIndex;

            // While there remain elements to shuffle.
            while (currentIndex != 0) {

                // Pick a remaining element.
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;

                // And swap it with the current element.
                [array[currentIndex], array[randomIndex]] = [
                    array[randomIndex], array[currentIndex]
                ];
            }

            return array;
        },
        handleFilePondInit: function () {
            console.log('FilePond has initialized');
        },
        clearModalMessage() {
            this.modalMessages = [];
            this.showModal = false;
            this.claimNumber = 0;
            this.evidenceNumber = 0;
            this.getDatabases();
            if (this.selectedDatabase != "") {
                this.getClaims(this.selectedDatabase)
            }
        },
        mainAddDatabase(e) {
            const pondFiles = this.$refs.pond.getFiles();
            this.addDatabase(e, pondFiles, "", true)
        },
        async addDatabase(e, pondFiles, databaseID, newFlag) {
            // Show the loading modal to indicate progress
            this.loadingAdd = true;
            this.showModal = true;
            // If there is json formatting issues, do not process that claim
            for (var i = 0; i < pondFiles.length; i++) {
                const fileLoad = await new Promise(resolve => {
                    this.fileReadObject = null;
                    const fileName = pondFiles[i].filename
                    const fr = new FileReader();
                    fr.readAsText(pondFiles[i].file);
                    var self = this;
                    fr.onload = async (e) => {
                        let text = e.target.result
                        try {
                            let result = JSON.parse(text);
                            console.log("JSON is valid");
                        } catch (e) {
                            self.toast.error("Please check the json formatting in the file named: " + fileName);
                            return
                        }
                        try {
                            const formData = new FormData();
                            formData.append('file', pondFiles[i].file);
                            formData.append('new', newFlag);
                            formData.append('owner', self.store.userid);
                            formData.append('name', self.databaseName);
                            formData.append('databaseId', databaseID);
                            formData.append('description', self.description);
                            formData.append('accesskey', self.databasePassword);
                            formData.append('salt', self.generateRandomSalt());
                            await axios.post(`${domain}/api/v1/database/newdb/`, formData, {
                                    headers: {
                                        'Content-Type': 'multipart/form-data'
                                    }
                                })
                                .then(response => {
                                    console.log(response.data);
                                    this.evidenceNumber = response.data.numEvidence;
                                    this.claimNumber = response.data.numClaim;
                                    // Handle response data as needed
                                })
                                .catch(error => {
                                    console.error(error);
                                });
                            console.log(formData)
                        } catch (error) {
                            // Handle errors that occur during file upload or processing
                            console.error(`Error processing file ${fileName}:`, error);
                            self.toast.error(`Error processing file ${fileName}: ${error.message}`);
                        }
                        resolve()
                    }
                });
            }
            this.loadingAdd = false;
        },
        async addClaimAndEvidenceManual(e) {
            const databaseId = this.selectedDatabase;

            if (this.uploadFiles) {
                const manualPondFiles = this.$refs.manualpond.getFiles();
                const added = await this.addDatabase(e, manualPondFiles, databaseId, false)
            } else {
                const claim = this.addClaimContent;
                const claimId = this.addClaimOriginalID;
                const evidences = this.addEvidenceStore;
                this.addClaims(databaseId, claim, claimId, evidences);
                this.toast.success("Claims and evidences added successfully.");
            }
        },
        addClaims(databaseId, claim, claimId, evidences) {
            const claimData = {
                database: databaseId,
                content: claim,
                original_id: claimId,
            }
            axios
                .post(`${domain}/api/v1/database/claims/create/`, claimData)
                .then(response => {
                    this.modalMessages.push("Successfully added claim: \"" + claim + "\" to database.")
                    //Add evidences
                    for (let k = 0; k < evidences.length; k++) {
                        this.addEvidence(response.data.id, evidences[k]);
                    }
                    this.getClaims(this.selectedDatabase)
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
        },
        // Main evidence add on database add page
        addEvidence(claimId, content) {
            const evidenceData = {
                claim: claimId,
                content: content,
            }
            console.log(evidenceData)
            axios
                .post(`${domain}/api/v1/database/evidence/create/`, evidenceData)
                .then(response => {
                    if (response.data.created == false) {
                        this.modalMessages.push("Evidence - " + content + " already exists. The evidence will not be added.")
                    } else {
                        this.evidenceNumber = this.evidenceNumber + 1;
                        this.modalMessages.push("Successfully added evidence - " + content + " to database.")
                    }
                    // Successfully added database, claims and evidences
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    this.modalMessages.push("There were some issues adding evidence - " + content + " .");
                })

        },
        getDatabases() {
            axios
                .get(`${domain}/api/v1/database/`)
                .then((response) => {
                    this.returnData = response.data
                    console.log(this.returnData)
                })
                .catch(error => {
                    // Request was made and server responded unfavourably
                    this.toast.error("There was some issue retrieving databases.");
                })
        },
        activateDatabase: function (e) {
            console.log(e.target.id.substring(9))
            const updatedData = {
                is_active: e.target.value,
            }
            axios
                .patch(`${domain}/api/v1/database/update/` + e.target.id.substring(9) + '/', updatedData)
                .then((response) => {
                    console.log(response.data)
                    this.getDatabases()
                    if (updatedData.is_active == "True") {
                        this.toast.success("Database is activated and ready for labelling.");
                    } else {
                        this.toast.success("Database is deactivated and labelling cannot be done.");
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
        },
        deleteDatabase: function (e) {
            axios
                .delete(`${domain}/api/v1/database/delete/` + e.target.id.substring(7) + '/')
                .then((response) => {
                    console.log(response.data)
                    this.getDatabases()
                    this.toast.success("Database is successfully deleted.");
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
        },
        changeSelectedDatabase(id, name) {
            this.selectedDatabase = id;
            this.$refs.selectDatabaseBtn.innerText = id + " - " + name;
            // Updates claims as well
            this.getClaims(this.selectedDatabase);
        },
        changeSelectedDatabaseAnnotation(id, name) {
            this.selectedDatabaseAnnotation = id;
            this.$refs.selectDatabaseBtnAnnotation.innerText = id + " - " + name;
            this.getFirstReviewableAnnotation();
        },
        getClaims(dbId) {
            axios
                .get(`${domain}/api/v1/database/claims/list/`, {
                    params: { databaseId: dbId }
                })
                .then((response) => {
                    console.log(response.data)
                    this.claimData = response.data
                    console.log(this.claimData)
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
        },
        // Delete claims
        deleteClaim: function (e) {
            axios
                .delete(`${domain}/api/v1/database/claims/delete/` + e.target.id.substring(7) + '/')
                .then((response) => {
                    console.log(response.data)
                    this.getClaims(this.selectedDatabase)
                    this.toast.success("Claim is successfully deleted.");
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
        },
        // Manual add evidence on add claims page to append to internal data lists
        addEvidenceConfirm() {
            this.addEvidenceStore.push(this.$refs.evidenceField.value)
        },
        deleteEvidenceConfirm: function (e) {
            const indexToDelete = e.target.id.substring(7)
            this.addEvidenceStore.splice(indexToDelete, 1)
        },
        getAnnotations() {
            axios
                .get(`${domain}/api/v1/database/annotation/list/`, {
                    params: { databaseId: this.selectedDatabaseAnnotation }
                })
                .then((response) => {
                    console.log(JSON.stringify(response.data))
                    var bb = new Blob([JSON.stringify(response.data)], { type: 'text/json' });
                    var a = document.createElement('a');
                    a.download = 'annotation_results.json';
                    a.href = window.URL.createObjectURL(bb);
                    a.click();
                    a.remove();
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
        },
        getFirstReviewableAnnotation() {
            this.currentAnnotation = "";
            this.submitted = false;
            this.selectedLabel = "";
            this.processing = true;
            axios
                .get(`${domain}/api/v1/database/annotation/list/review/`, {
                    params: { databaseId: this.selectedDatabaseAnnotation }
                })
                .then((response) => {
                    if (!response.data.data || response.data.data.length === 0) {
                        this.processing = false;
                        console.log(response.data)
                        return;
                    }
                    this.currentAnnotation = response.data.data;
                    this.currentAnnotation.annotations.annotated_at = this.currentAnnotation.annotations.annotated_at
                    const dateObject = new Date(this.currentAnnotation.annotations.annotated_at);
                    const formattedDate = dateObject.toLocaleDateString();
                    const formattedTime = dateObject.toLocaleTimeString();
                    this.currentAnnotation.annotations.annotated_at = `${formattedDate} ${formattedTime}`;
                    this.submitted = false;
                    this.processing = false;
                    this.selectedLabel = "";
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
        },
        removeAnnotation(id, label) {
            id = parseInt(id);
            console.log(this.currentAnnotation.annotations[0].id)
            this.currentAnnotation.annotations = this.currentAnnotation.annotations.filter((annotation) => annotation.id !== id);
            console.log(this.currentAnnotation.annotations)
            console.log(label)
            if (label in this.currentAnnotation.evidence.label_counts) {
                this.currentAnnotation.evidence.label_counts[label]--;
            } else if (label == "NOT ENOUGH INFORMATION") {
                if ("NOT ENOUGH INFO" in this.currentAnnotation.evidence.label_counts) {
                    this.currentAnnotation.evidence.label_counts["NOT ENOUGH INFO"]--;
                }
            }
        },
        ignoreAnnotation(e, label) {
            const annotationData = {
                database_id: this.selectedDatabaseAnnotation,
                annotation_id: e.target.id.substring(10),
            }
            axios
                .post(`${domain}/api/v1/database/annotation/ignore/`, annotationData)
                .then((response) => {
                    console.log(response.data)
                    this.toast.success("Successfully ignored annotation.");
                    this.removeAnnotation(annotationData.annotation_id, label)
                }).catch(error => {
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
        ignoreAnnotator(e, id, label) {
            const annotationData = {
                database_id: this.selectedDatabaseAnnotation,
                annotator_email: e.target.id.substring(10),
            }
            axios
                .post(`${domain}/api/v1/database/annotation/ignoreall/`, annotationData)
                .then((response) => {
                    console.log(response.data)
                    this.toast.success("Successfully ignored all annotations.");
                    this.removeAnnotation(id, label);

                }).catch(error => {
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
        updateFinal() {
            this.submitted = true;
            this.paraphraseFlag = true;
            const evidenceData = {
                claim_id: this.currentAnnotation.claim.id,
                evidence_id: this.currentAnnotation.evidence.id,
                final_label: this.selectedLabel,
            }
            console.log(evidenceData)
            axios
                .post(`${domain}/api/v1/database/evidence/updateFinal/`, evidenceData)
                .then((response) => {
                    console.log(response.data)
                    this.toast.success("Successfully recorded final label for evidence.");
                    this.paraphrases = response.data.paraphrases;
                    console.log(this.paraphrases)
                }).catch(error => {
                    console.log(error)
                    // Request was made and server responded unfavourably
                    this.paraphraseFlag = false;
                })
            },
            async downloadJson() {
                try {
                    const response = await axios.get(`${domain}/api/v1/database/annotation/final/`);
                    const data = response.data;
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    saveAs(blob, 'data.json');
                } catch (error) {
                    console.error('Error downloading JSON:', error);
                }
            },

    },
    components: {
        FilePond,
    },
}
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css");

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.upload {
    margin-top: 30px;
}

.form-check-label {
    margin-left: 15px;
    margin-top: 10px;
}

#flexSwitchCheckChecked {
    width: 40px;
    height: 40px;
}

.password_validation {
    margin-top: 15px;
}

.view-database-label {
    padding-top: 10px;
    margin-bottom: 10px;
}

.list-database {
    height: 600px;
    background-color: white;
    border-radius: 5px;
}

.list-group-item {
    background-color: #faf5f5;
    margin-bottom: 5px;
}

.options {
    margin-top: auto;
    margin-bottom: auto;
}

.delete-button {
    margin-left: 10px;
}

.listtransition-enter-active,
.listtransition-leave-active {
    transition: all 1s;
}

.listtransition-enter,
.listtransition-leave-to {
    opacity: 0;
    transform: translateX(-295px);
}

.form-switch.form-switch-lg {
    margin-bottom: 1.5rem;
    /* JUST FOR STYLING PURPOSE */
    width: 100%;
}

.form-switch.form-switch-lg .form-check-input {
    height: 2rem;
    width: calc(3rem + 0.75rem);
    border-radius: 4rem;
}

.form-check-label {
    margin-left: 30px;
}

.evidences {
    margin-top: 20px;
    width: 100%;
    height: 200px;
    border: 1px solid rgb(210, 210, 210);
}

.model-message {
    height: 300px;
    background-color: #f5f2f2;
    padding: 10px;
    border-radius: 5px;
}

.message-list {
    border-radius: 5px;
    background-color: white;
    border: 1px #c2c0c0 solid;
    padding: 5px;
    margin-top: 5px;
}

.numberClaims {
    font-size: 14px;
    font-weight: 400;
}

.logout-button {
    width: 200px;
}

.claim-text {
    font-weight: 800;
}

.ignore {
    margin-top: 10px;
    width: 40%;
    font-weight: 600;
    font-size: 15px;
    background-color: rgba(209, 208, 208, 0.599);
    color: rgb(99, 99, 99);
    border: none;
    border-radius: 0px;
}

.ignore:hover {
    background-color: rgb(70, 70, 70);
    color: white;
}

.annotation-stats {
    display: flex;
    justify-content: space-around;
    width: 100%;
    background-color: #f8f6f6fc;
    border-radius: 5px;
}

.stat-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 24px;
    color: white;
}

.stat-circle span {
    position: absolute;
    font-size: 18px;
}

.supports {
    background-color: #28a745;
}

.refutes {
    background-color: #dc3545;
}

.not-enough-info {
    background-color: #ffc107;
}

.annotation_numbers {
    font-weight: 600;
}

.annotation-label {
    font-weight: 600;
    font-size: 18px;
}

.label-text {
    font-size: 15px;
    text-align: center;
    color: black;
    font-weight: 600;
}

.gpt {
    background-color: #f5f2f2;
}

.left-annotation {
    background-color: #f5f2f2;
}

.gpt_label {
    font-weight: 600;
    font-size: 18px;
    background-color: rgb(140, 140, 140);
    color: white;
    padding: 10px;
    margin-bottom: 20px;
}

.final-select {
    border: none;
    border-radius: 5px;
    padding: 20px;
    padding-right: 30px;
    appearance: none;
    background-position: right 0.5em top 50%;
    background-size: 8px 10px;
}

.final-select option {
    background-color: white;
}

.submit-final {
    background: none;
}

.submit-final:hover {
    background-color: #c2c0c0;
}

.submit-final-icon {
    font-size: 27px;
}

.getNext {
    background-color: #bababa;
    padding: 10px;
    width: 100%;
    text-align: center;
    color: white;
    font-weight: 800;
    font-size: 18px;
}

/* @import '../assets/css/homepage.css'; */
</style>
