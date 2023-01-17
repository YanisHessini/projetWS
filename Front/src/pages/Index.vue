<script setup lang="ts">
import Header from '../components/Header.vue';
</script>

<template>
	<Header></Header>
	<!-- Welcome text -->
	<div class="flex justify-center">
		<div class="text-center justify-center items-center">
			<div class="flex justify-center items-center">
				<img
					src="https://img.freepik.com/vecteurs-libre/illustration-concept-abstrait-transport-grande-vitesse_335657-3926.jpg?w=2000"
					class="max-w-sm object-scale-down">
			</div>
			<h1 class="text-5xl font-bold m-4">Bienvenue sur TrainsNow</h1>
			<p class="text-2xl font-medium">Le meilleur outil pour trouver et réserver des trains</p>
			<button 
				class="bg-green-500 text-white text-xl px-10 py-1.5 mt-5 rounded-full font-medium hover:bg-opacity-75">
			<router-link to="/list">Réserver maintenant</router-link>
			</button>
			<button 
				class="bg-green-500 text-white text-xl px-10 py-1.5 mt-5 ml-10 rounded-full font-medium hover:bg-opacity-75">
			<router-link to="/reservations">Voir mes réservations</router-link>
			</button>
		</div>
	</div>

</template>
