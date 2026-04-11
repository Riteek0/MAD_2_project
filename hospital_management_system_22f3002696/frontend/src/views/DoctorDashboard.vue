<template>
  <div>

    <!-- Navbar -->
    <nav class="navbar px-4 py-3" style="background:#1e1e2f;">
      <span class="fw-bold fs-5" style="color:#a78bfa;">Doctor Dashboard</span>
      <div class="d-flex gap-2">
        <button
          class="btn btn-sm"
          style="background:#7c3aed;color:#fff;border:none;"
          @click="openEditProfile"
        >Edit Profile</button>
        <button
          class="btn btn-sm"
          style="background:#ef4444;color:#fff;border:none;"
          @click="logout"
        >Logout</button>
      </div>
    </nav>

    <div class="container mt-4">

      <!-- Welcome -->
      <h5 class="mb-4" style="color:#1e1e2f;">Welcome, {{ name }}</h5>

      <!-- Stats Cards -->
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm text-white text-center py-3"
            style="background:#4f46e5;">
            <p class="mb-1 small fw-semibold">Total Appointments</p>
            <h3 class="fw-bold mb-0">{{ stats.total_appointments }}</h3>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm text-white text-center py-3"
            style="background:#d97706;">
            <p class="mb-1 small fw-semibold">Pending</p>
            <h3 class="fw-bold mb-0">{{ stats.pending }}</h3>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm text-white text-center py-3"
            style="background:#059669;">
            <p class="mb-1 small fw-semibold">Completed</p>
            <h3 class="fw-bold mb-0">{{ stats.completed }}</h3>
          </div>
        </div>
      </div>

      <!-- Set Availability -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-header border-0 fw-semibold"
          style="background:#f0f4ff;color:#3730a3;">
          Set Availability (Next 7 Days Only)
        </div>
        <div class="card-body">
          <p class="text-muted small mb-3">
            Add your available time slots. Dates restricted to next 7 days only.
          </p>

          <div
            v-for="(slot, index) in availability"
            :key="index"
            class="row g-2 align-items-center mb-2"
          >
            <div class="col-md-4">
              <input
                v-model="slot.date"
                type="date"
                class="form-control form-control-sm"
                :min="minDate"
                :max="maxDate"
                style="border-color:#c7d2fe;"
              />
            </div>
            <div class="col-md-3">
              <input
                v-model="slot.start"
                type="time"
                class="form-control form-control-sm"
                style="border-color:#c7d2fe;"
                placeholder="Start"
              />
            </div>
            <div class="col-md-3">
              <input
                v-model="slot.end"
                type="time"
                class="form-control form-control-sm"
                style="border-color:#c7d2fe;"
                placeholder="End"
              />
            </div>
            <div class="col-md-2">
              <button
                class="btn btn-sm w-100"
                style="background:#fee2e2;color:#dc2626;border:none;"
                @click="removeSlot(index)"
              >Remove</button>
            </div>
          </div>

          <p v-if="!availability.length" class="text-muted small">
            No availability saved yet.
          </p>

          <p v-if="availMsg" class="text-success small mt-2">{{ availMsg }}</p>
          <p v-if="availErr" class="text-danger small mt-2">{{ availErr }}</p>

          <div class="d-flex gap-2 mt-3">
            <button
              class="btn btn-sm"
              style="background:#e0e7ff;color:#4f46e5;border:none;"
              @click="addSlot"
            >+ Add Slot</button>
            <button
              class="btn btn-sm"
              style="background:#059669;color:#fff;border:none;"
              @click="saveAvailability"
            >Save Availability</button>
          </div>
        </div>
      </div>

      <!-- My Appointments -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-header border-0 fw-semibold"
          style="background:#f0f4ff;color:#3730a3;">
          My Appointments
        </div>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead style="background:#1e1e2f;color:#fff;">
              <tr>
                <th>#</th>
                <th>Patient</th>
                <th>Date</th>
                <th>Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in appointments" :key="a.id">
                <td>{{ a.id }}</td>
                <td>{{ a.patient_name }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td>
                  <span
                    class="badge"
                    :style="a.status === 'completed'
                      ? 'background:#dcfce7;color:#166534;'
                      : a.status === 'cancelled'
                      ? 'background:#fee2e2;color:#991b1b;'
                      : 'background:#fef3c7;color:#92400e;'"
                  >{{ a.status }}</span>
                </td>
                <td>
                  <div class="d-flex gap-2">
                    <button
                      v-if="a.status === 'pending'"
                      class="btn btn-sm"
                      style="background:#059669;color:#fff;border:none;"
                      @click="completeAppointment(a.id)"
                    >Complete</button>
                    <button
                      v-if="a.status === 'pending'"
                      class="btn btn-sm"
                      style="background:#fef2f2;color:#dc2626;border:1px solid #fca5a5;"
                      @click="cancelAppointment(a.id)"
                    >Cancel</button>
                    <button
                      class="btn btn-sm"
                      style="background:#e0e7ff;color:#4f46e5;border:none;"
                      @click="openTreatment(a)"
                    >Treatment</button>
                  </div>
                </td>
              </tr>
              <tr v-if="!appointments.length">
                <td colspan="6" class="text-center text-muted py-3">
                  No appointments yet
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- Treatment Modal -->
    <div v-if="treatmentModal"
      class="modal d-block"
      style="background:rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content border-0 shadow">
          <div class="modal-header" style="background:#1e1e2f;">
            <h6 class="modal-title" style="color:#a78bfa;">
              Add Treatment — {{ selectedAppointment?.patient_name }}
            </h6>
            <button class="btn-close btn-close-white"
              @click="treatmentModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label text-muted small">Diagnosis</label>
              <input
                v-model="treatment.diagnosis"
                class="form-control"
                style="border-color:#c7d2fe;"
                placeholder="Enter diagnosis"
              />
            </div>
            <div class="mb-2">
              <label class="form-label text-muted small">Prescription</label>
              <textarea
                v-model="treatment.prescription"
                class="form-control"
                rows="2"
                style="border-color:#c7d2fe;"
                placeholder="Enter prescription"
              ></textarea>
            </div>
            <div class="mb-2">
              <label class="form-label text-muted small">Notes</label>
              <textarea
                v-model="treatment.notes"
                class="form-control"
                rows="2"
                style="border-color:#c7d2fe;"
                placeholder="Additional notes"
              ></textarea>
            </div>
            <div class="mb-2">
              <label class="form-label text-muted small">Next Visit Date</label>
              <input
                v-model="treatment.next_visit_date"
                type="date"
                class="form-control"
                style="border-color:#c7d2fe;"
              />
            </div>
            <p v-if="treatmentMsg" class="text-success small mt-1">{{ treatmentMsg }}</p>
            <p v-if="treatmentErr" class="text-danger small mt-1">{{ treatmentErr }}</p>
          </div>
          <div class="modal-footer">
            <button
              class="btn"
              style="background:#4f46e5;color:#fff;border:none;"
              @click="saveTreatment"
            >Save Treatment</button>
            <button
              class="btn"
              style="background:#64748b;color:#fff;border:none;"
              @click="treatmentModal = false"
            >Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="editModal"
      class="modal d-block"
      style="background:rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content border-0 shadow">
          <div class="modal-header" style="background:#1e1e2f;">
            <h6 class="modal-title" style="color:#a78bfa;">Edit Profile</h6>
            <button class="btn-close btn-close-white"
              @click="editModal = false"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Full Name</label>
              <input v-model="profile.name" class="form-control"
                style="border-color:#c7d2fe;" />
            </div>
            <div class="mb-2">
              <label class="form-label">Specialization</label>
              <input v-model="profile.specialization" class="form-control"
                style="border-color:#c7d2fe;" />
            </div>
            <p v-if="profileMsg" class="text-success small">{{ profileMsg }}</p>
          </div>
          <div class="modal-footer">
            <button
              class="btn"
              style="background:#7c3aed;color:#fff;border:none;"
              @click="saveProfile"
            >Save</button>
            <button
              class="btn"
              style="background:#64748b;color:#fff;border:none;"
              @click="editModal = false"
            >Cancel</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      name:         localStorage.getItem('name'),
      stats:        { total_appointments: 0, pending: 0, completed: 0 },
      appointments: [],
      availability: [],
      minDate:      '',
      maxDate:      '',
      availMsg:     '',
      availErr:     '',

      treatmentModal:      false,
      selectedAppointment: null,
      treatment: {
        diagnosis:       '',
        prescription:    '',
        notes:           '',
        next_visit_date: ''
      },
      treatmentMsg: '',
      treatmentErr: '',

      editModal:  false,
      profile:    { name: '', specialization: '' },
      profileMsg: ''
    }
  },

  async mounted() {
    this.setDateRange()
    await this.loadDashboard()
    await this.loadAppointments()
    await this.loadAvailability()
  },

  methods: {
    headers() {
      return { Authorization: `Bearer ${localStorage.getItem('token')}` }
    },

    setDateRange() {
      const today = new Date()
      const max   = new Date()
      max.setDate(today.getDate() + 7)
      this.minDate = today.toISOString().split('T')[0]
      this.maxDate = max.toISOString().split('T')[0]
    },

    async loadDashboard() {
      try {
        const res    = await axios.get('http://127.0.0.1:5000/api/doctor/dashboard',
          { headers: this.headers() })
        this.stats   = res.data
      } catch (e) {
        if (e.response?.status === 401) {
          localStorage.clear()
          this.$router.push('/login')
        }
      }
    },

    async loadAppointments() {
      try {
        const res        = await axios.get('http://127.0.0.1:5000/api/doctor/appointments',
          { headers: this.headers() })
        this.appointments = res.data
      } catch (e) {
        console.error('Failed to load appointments')
      }
    },

    async loadAvailability() {
      try {
        const res        = await axios.get('http://127.0.0.1:5000/api/doctor/dashboard',
          { headers: this.headers() })
        this.availability = res.data.availability || []
      } catch (e) {
        this.availability = []
      }
    },

    addSlot() {
      this.availability.push({ date: '', start: '', end: '' })
    },

    removeSlot(index) {
      this.availability.splice(index, 1)
    },

    async saveAvailability() {
      this.availMsg = ''
      this.availErr = ''
      for (const slot of this.availability) {
        if (!slot.date || !slot.start || !slot.end) {
          this.availErr = 'Please fill date, start and end time for all slots'
          return
        }
        if (slot.date < this.minDate || slot.date > this.maxDate) {
          this.availErr = 'All dates must be within the next 7 days'
          return
        }
      }
      try {
        await axios.put(
          'http://127.0.0.1:5000/api/doctor/set-availability',
          { availability: this.availability },
          { headers: this.headers() }
        )
        this.availMsg = 'Availability saved successfully'
        setTimeout(() => this.availMsg = '', 3000)
      } catch (e) {
        this.availErr = 'Failed to save availability'
      }
    },

    async completeAppointment(id) {
      if (!confirm('Mark this appointment as completed?')) return
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/doctor/appointment/${id}/complete`,
          {}, { headers: this.headers() }
        )
        await this.loadDashboard()
        await this.loadAppointments()
      } catch (e) {
        alert('Failed to complete appointment')
      }
    },

    async cancelAppointment(id) {
      if (!confirm('Cancel this appointment?')) return
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/doctor/appointment/${id}/cancel`,
          {}, { headers: this.headers() }
        )
        await this.loadDashboard()
        await this.loadAppointments()
      } catch (e) {
        alert('Failed to cancel appointment')
      }
    },

    openTreatment(appointment) {
      this.selectedAppointment = appointment
      this.treatment = {
        diagnosis:       '',
        prescription:    '',
        notes:           '',
        next_visit_date: ''
      }
      this.treatmentMsg  = ''
      this.treatmentErr  = ''
      this.treatmentModal = true
    },

    async saveTreatment() {
      this.treatmentMsg = ''
      this.treatmentErr = ''
      try {
        await axios.post(
          `http://127.0.0.1:5000/api/doctor/treatment/${this.selectedAppointment.id}`,
          this.treatment,
          { headers: this.headers() }
        )
        this.treatmentMsg = 'Treatment saved successfully'
        setTimeout(() => {
          this.treatmentModal = false
          this.treatmentMsg   = ''
        }, 1200)
      } catch (e) {
        this.treatmentErr = 'Failed to save treatment'
      }
    },

    openEditProfile() {
      this.profile    = { name: localStorage.getItem('name') || '', specialization: '' }
      this.profileMsg = ''
      this.editModal  = true
    },

    async saveProfile() {
      try {
        await axios.put(
          'http://127.0.0.1:5000/api/doctor/profile',
          this.profile,
          { headers: this.headers() }
        )
        this.profileMsg = 'Profile updated successfully'
        localStorage.setItem('name', this.profile.name)
        this.name = this.profile.name
        setTimeout(() => {
          this.editModal  = false
          this.profileMsg = ''
        }, 1200)
      } catch (e) {
        alert('Failed to update profile')
      }
    },

    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>