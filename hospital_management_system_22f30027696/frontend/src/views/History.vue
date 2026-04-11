<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>My Treatment History</h5>
      <router-link to="/patient" class="btn btn-sm btn-outline-secondary">← Back</router-link>
    </div>
    <table class="table table-bordered shadow-sm">
      <thead class="table-dark">
        <tr><th>#</th><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th><th>Diagnosis</th><th>Prescription</th><th>Next Visit</th></tr>
      </thead>
      <tbody>
        <tr v-for="a in history" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.doctor_name }}</td>
          <td>{{ a.date }}</td>
          <td>{{ a.time }}</td>
          <td>
            <span :class="{
              'badge bg-warning text-dark': a.status==='pending',
              'badge bg-success': a.status==='completed',
              'badge bg-danger': a.status==='cancelled'
            }">{{ a.status }}</span>
          </td>
          <td>{{ a.diagnosis || '—' }}</td>
          <td>{{ a.prescription || '—' }}</td>
          <td>{{ a.next_visit_date || '—' }}</td>
        </tr>
        <tr v-if="!history.length">
          <td colspan="8" class="text-center text-muted">No history found</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() { return { history: [] } },
  async mounted() {
    const res = await axios.get('http://127.0.0.1:5000/api/patient/history', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    this.history = res.data
  }
}
</script>