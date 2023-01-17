<script setup lang="ts">
// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
	document.documentElement.classList.add('dark');
} else {
	document.documentElement.classList.remove('dark')
}


</script>

<template>
	<header class="bg-gray-900 text-white p-4 flex justify-between items-center">
		<div class="flex items-center">
			<a href="#" class="text-2xl font-medium mr-4">
				<router-link to="/">TrainsNow</router-link>
			</a>
			<nav>
				<!-- <a href="#" class="text-sm font-medium mr-4 ">Home</a>
            <a href="#" class="text-sm font-medium mr-4">About</a>
            <a href="#" class="text-sm font-medium">Contact</a> -->
			</nav>
		</div>
	</header>
</template>