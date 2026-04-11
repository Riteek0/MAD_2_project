<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>All Appointments</h5>
      <router-link to="/admin" class="btn btn-sm btn-outline-secondary">← Back</router-link>
    </div>
    <table class="table table-bordered table-hover shadow-sm">
      <thead class="table-dark">
        <tr><th>#</th><th>Patient</th><th>Doctor</th><th>Date</th><th>Time</th><th>Status</th></tr>
      </thead>
      <tbody>
        <tr v-for="a in appointments" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.patient_name }}</td>
          <td>{{ a.doctor_name }}</td>
          <td>{{ a.date }}</td>
          <td>{{ a.time }}</td>
          <td>
            <span :class="{
              'badge bg-warning text-dark': a.status === 'pending',
              'badge bg-success': a.status === 'completed',
              'badge bg-danger': a.status === 'cancelled'
            }">{{ a.status }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() { return { appointments: [] } },
  async mounted() {
    const res = await axios.get('http://127.0.0.1:5000/api/admin/appointments', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    this.appointments = res.data
  }
}
</script>