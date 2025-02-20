<template>
  <tr
    :class="{ dropzone: dropZone }"
    @drop.stop="onDrop($event)"
    @dragover.prevent="isDropZone($event, true)"
    @dragenter.prevent="isDropZone($event, true)"
    @dragleave.prevent="isDropZone($event, false)"
  >
    <td class="font-weight-medium pl-8">
      <router-link
        :to="{
          name: 'Organization',
          params: { name: encodeURIComponent(name) },
        }"
        target="_blank"
        class="link--underline"
      >
        {{ name }}
      </router-link>
    </td>
    <td class="text-right text--secondary">
      <v-tooltip bottom transition="expand-y-transition" open-delay="200">
        <template v-slot:activator="{ on }">
          <v-btn
            depressed
            color="transparent"
            v-on="on"
            @click.stop="$emit('getEnrollments')"
          >
            {{ enrollments }}
            <v-icon small right> mdi-account-multiple </v-icon>
          </v-btn>
        </template>
        <span>Enrollments</span>
      </v-tooltip>
    </td>
    <td class="text-right">
      <v-menu v-model="showMenu" left nudge-left="16">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon small v-bind="attrs" v-on="on">
            <v-icon small>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item @click="$emit('edit')">
            <v-list-item-title> View/edit domains </v-list-item-title>
          </v-list-item>
          <v-edit-dialog
            large
            @save="
              $emit('addTeam', newTeam);
              newTeam = '';
            "
            @cancel="newTeam = ''"
          >
            <v-list-item @click="showMenu = false">
              <v-list-item-title>Add a team</v-list-item-title>
            </v-list-item>
            <template v-slot:input>
              <h6 class="text-subtitle-2 mt-2">Add team to {{ name }}</h6>
              <v-text-field
                v-model="newTeam"
                label="Name"
                maxlength="50"
                single-line
              />
            </template>
          </v-edit-dialog>
          <v-list-item @click="$emit('delete')">
            <v-list-item-title>Delete organization</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn icon @click.stop="$emit('expand')">
        <v-icon>
          {{ isExpanded ? "mdi-chevron-up" : "mdi-chevron-down" }}
        </v-icon>
      </v-btn>
    </td>
  </tr>
</template>

<script>
export default {
  name: "OrganizationEntry",
  props: {
    name: {
      type: String,
      required: true,
    },
    enrollments: {
      type: Number,
      required: true,
    },
    isExpanded: {
      type: Boolean,
      required: true,
    },
    isEditable: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data() {
    return {
      dropZone: false,
      showMenu: false,
      newTeam: "",
    };
  },
  methods: {
    onDrop(event) {
      this.dropZone = false;
      const organization = event.dataTransfer.getData("group");
      const isTeam = event.dataTransfer.types.includes("parentorg");
      const individuals = event.dataTransfer.getData("individuals");

      if (organization && organization !== this.name && !isTeam) {
        this.$emit("merge:orgs", {
          fromOrg: organization,
          toOrg: this.name,
        });
      } else if (individuals) {
        const droppedIndividuals = JSON.parse(individuals).filter(
          (individual) => !individual.isLocked
        );
        if (droppedIndividuals.length > 0) {
          this.$emit("enroll", {
            individuals: droppedIndividuals,
            group: this.name,
          });
        }
      }
    },
    isDropZone(event, isDragging) {
      const types = event.dataTransfer.types;
      this.dropZone =
        isDragging &&
        !types.includes("lockactions") &&
        !types.includes("parentorg");
    },
  },
};
</script>
<style lang="scss" scoped>
@import "../styles/index.scss";
tr {
  cursor: pointer;
}

td:last-of-type {
  width: 100px;
}

tr[draggable="true"] {
  td:first-of-type {
    position: relative;

    &::before {
      font: normal normal normal 24px/1 "Material Design Icons";
      font-size: 1rem;
      content: "\F01DD";
      color: rgba(0, 0, 0, 0.62);
      position: absolute;
      left: 4px;
      top: 30%;
      opacity: 0;
      cursor: grab;
    }
  }

  &:hover td::before {
    opacity: 1;
  }
}
</style>
