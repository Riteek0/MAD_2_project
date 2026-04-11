<template>
  <div class="container mt-5">
    <div class="card border-0 shadow-sm mx-auto" style="max-width:480px;">

      <div class="card-header border-0 fw-semibold"
        style="background:#f0f4ff;color:#3730a3;">
        Book Appointment
      </div>

      <div class="card-body">

        <!-- Doctor Name (read-only) -->
        <div class="mb-3">
          <label class="form-label text-muted small">Doctor</label>
          <input
            class="form-control"
            :value="doctorName"
            readonly
            style="background:#f8fafc;border-color:#c7d2fe;color:#1e1e2f;"
          />
        </div>

        <!-- Date -->
        <div class="mb-3">
          <label class="form-label text-muted small">Date</label>
          <input
            v-model="form.date"
            type="date"
            class="form-control"
            :min="minDate"
            :max="maxDate"
            style="border-color:#c7d2fe;"
          />
        </div>

        <!-- Time -->
        <div class="mb-3">
          <label class="form-label text-muted small">Time</label>
          <input
            v-model="form.time"
            type="time"
            class="form-control"
            style="border-color:#c7d2fe;"
          />
        </div>

        <!-- Messages -->
        <p v-if="err" class="text-danger small">{{ err }}</p>
        <p v-if="msg" class="text-success small">{{ msg }}</p>

        <!-- Book Button -->
        <button
          class="btn w-100 fw-semibold"
          style="background:#4f46e5;color:#fff;border:none;"
          @click="book"
          :disabled="loading"
        >
          {{ loading ? 'Booking...' : 'Book Now' }}
        </button>

        <!-- Back -->
        <div class="text-center mt-3">
          <router-link to="/patient" class="text-muted small">
            Back to Dashboard
          </router-link>
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
      doctorName: this.$route.query.doctor_name || 'Unknown Doctor',
      doctorId:   this.$route.query.doctor_id,
      form: {
        date: '',
        time: ''
      },
      minDate: '',
      maxDate: '',
      loading: false,
      err: '',
      msg: ''
    }
  },

  mounted() {
    this.setDateRange()
  },

  methods: {
    setDateRange() {
      const today = new Date()
      const max   = new Date()
      max.setDate(today.getDate() + 7)
      this.minDate = today.toISOString().split('T')[0]
      this.maxDate = max.toISOString().split('T')[0]
    },

    async book() {
      this.err = ''
      this.msg = ''

      if (!this.doctorId) {
        this.err = 'Doctor not selected. Please go back and select a doctor.'
        return
      }
      if (!this.form.date) {
        this.err = 'Please select a date'
        return
      }
      if (!this.form.time) {
        this.err = 'Please select a time'
        return
      }

      this.loading = true
      try {
        const res = await axios.post(
          'http://127.0.0.1:5000/api/patient/book',
          {
            doctor_id: this.doctorId,
            date:      this.form.date,
            time:      this.form.time
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }
        )
        this.msg = res.data.message
        setTimeout(() => this.$router.push('/patient'), 1500)
      } catch (e) {
        this.err = e.response?.data?.error || 'Booking failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>