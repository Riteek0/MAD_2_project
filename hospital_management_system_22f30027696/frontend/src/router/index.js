import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import DoctorDashboard from '../views/DoctorDashboard.vue'
import PatientDashboard from '../views/PatientDashboard.vue'
import Booking from '../views/Booking.vue'
import History from '../views/History.vue'
import ViewDoctors from '../views/ViewDoctors.vue'
import ViewAppointments from '../views/ViewAppointments.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin', component: AdminDashboard },
  { path: '/doctor', component: DoctorDashboard },
  { path: '/patient', component: PatientDashboard },
  { path: '/book', component: Booking },
  { path: '/history', component: History },
  { path: '/admin/doctors', component: ViewDoctors },
  { path: '/admin/appointments', component: ViewAppointments }
]

export default createRouter({
  history: createWebHistory(),
  routes
})