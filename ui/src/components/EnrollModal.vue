<template>
  <v-dialog v-model="isOpen" max-width="550px">
    <v-card class="pa-3">
      <v-card-title class="headline">{{ title }}</v-card-title>
      <v-card-text>
        <p v-if="text" class="pt-2 pb-2 text-body-2">
          {{ text }}
        </p>
        <h6 v-if="organization" class="subheader">
          Enrollment dates (optional)
        </h6>
        <v-row>
          <v-col v-if="!organization" cols="4">
            <organization-selector
              v-model="form.organization"
              :fetch-organizations="fetchOrganizations"
            />
          </v-col>
          <v-col :cols="organization ? 6 : 4">
            <date-input v-model="form.dateFrom" label="Date from" outlined />
          </v-col>
          <v-col :cols="organization ? 6 : 4">
            <date-input v-model="form.dateTo" label="Date to" outlined />
          </v-col>
        </v-row>
        <v-alert v-if="errorMessage" text type="error">
          {{ errorMessage }}
        </v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="onClose"> Cancel </v-btn>
        <v-btn
          :disabled="!organization && !form.organization"
          color="primary"
          id="confirm"
          depressed
          @click="onSave"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DateInput from "./DateInput.vue";
import OrganizationSelector from "./OrganizationSelector.vue";

export default {
  name: "EnrollModal",
  components: { DateInput, OrganizationSelector },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    enroll: {
      type: Function,
      required: true,
    },
    uuid: {
      type: String,
      required: false,
    },
    title: {
      type: String,
      required: false,
    },
    text: {
      type: String,
      required: false,
    },
    organization: {
      type: String,
      required: false,
    },
    fetchOrganizations: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      form: {
        organization: this.organization,
        dateFrom: "",
        dateTo: "",
      },
      errorMessage: "",
    };
  },
  methods: {
    async onSave() {
      try {
        await this.enroll(
          this.uuid,
          this.form.organization,
          this.form.dateFrom,
          this.form.dateTo
        );
        this.onClose();
      } catch (error) {
        this.errorMessage = this.$getErrorMessage(error);
        this.$logger.error(`Error enrolling individual: ${error}`, this.form);
      }
    },
    onClose() {
      this.$emit("update:isOpen", false);
      this.form = {
        organization: this.organization,
        dateFrom: "",
        dateTo: "",
      };
      this.errorMessage = "";
    },
  },
  watch: {
    organization(value) {
      this.form.organization = value;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../styles/index.scss";
</style>
