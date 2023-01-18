<script setup lang="ts">

import Header from '../../components/Header.vue';
import soapRequest from 'easy-soap-request';
import { Icon } from '@iconify/vue';


const url = "http://127.0.0.1:8050/"

const modal = reactive({
	id: "1",
})

const trains = reactive({
	trainsJson: [],
	displayJson: JSON.parse('[]'),
	loading: true
});

// Function to get the list of trains with soap
const getTrains = async (event:any) => {
	try {
		event.preventDefault()
		if(event.target.tripStart.value === '')
			return

		console.log(event.target.tripStart.value)
		trains.trainJson = []
		trains.displayJson = JSON.parse('[]')
		trains.loading = true

		const getheaders = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'GetTrainsByDate',
			'Accept': 'text/xml',
		};
		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:GetTrainsByDate>
				 	<tns:startDate>${event.target.tripStart.value.toString()}</tns:startDate>
				</tns:GetTrainsByDate>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: getheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
		const { headers, body, statusCode } = response;

		// Isolate	 <trainsJson> from the response
		trains.trainsJson = body.substring(body.indexOf("<trainsJson>") + 12, body.indexOf("</trainsJson>"));
		// Parse the string that has &quot

		trains.trainsJson = JSON.parse(trains.trainsJson.replace(/&quot;/g, '"'));

		// Fill displayJson with the columns we want
		// basic number, departure_station, departure_date, arrival_station, arrival_date, total_seats

		for (let i = 0; i < trains.trainsJson.length; i++) {
			trains.displayJson.push({
				"id": trains.trainsJson[i].id,
				"departure_station": trains.trainsJson[i].departure_station,
				"departure_date": trains.trainsJson[i].departure_date,
				"arrival_station": trains.trainsJson[i].arrival_station,
				"arrival_date": trains.trainsJson[i].arrival_date,
				"available_seats": trains.trainsJson[i].available_seats,
			});
		}

		console.log(trains.displayJson);
		trains.loading = false;

	} catch (e) {
		console.log(e);
	}
};

// Function to get the list of trains with soap
const getAllTrains = async () => {
	try {
		const getheaders = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'GetAllTrains',
			'Accept': 'text/xml',
		};
		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:GetAllTrains/>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: getheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
		const { headers, body, statusCode } = response;

		console.log(body.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>'))

		// Isolate	 <trainsJson> from the response
		trains.trainsJson = body.substring(body.indexOf("<trainsJson>") + 12, body.indexOf("</trainsJson>"));
		// Parse the string that has &quot

		trains.trainsJson = JSON.parse(trains.trainsJson.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>'));

		// Fill displayJson with the columns we want
		// basic number, departure_station, departure_date, arrival_station, arrival_date, total_seats

		for (let i = 0; i < trains.trainsJson.length; i++) {
			trains.displayJson.push({
				"id": trains.trainsJson[i].id,
				"departure_station": trains.trainsJson[i].departure_station,
				"departure_date": trains.trainsJson[i].departure_date,
				"arrival_station": trains.trainsJson[i].arrival_station,
				"arrival_date": trains.trainsJson[i].arrival_date,
				"available_seats": trains.trainsJson[i].available_seats,
			});
		}

		console.log(trains.displayJson);
		trains.loading = false;

	} catch (e) {
		console.log(e);
	}
};



const changeModalId = (id) => {
	console.log(modal.id);
	console.log(id);
	modal.id = id;
	console.log(modal.id)
}



onMounted(() => {
	getAllTrains();
});

// Function to fill table html with id trains-list with data from JSON


</script>

<template>
	<Header></Header>

	<!-- Welcome text to view the list of trains -->
	<div class="flex flex-col justify-center items-center mt-10">
		<h1 class="text-4xl text-slate-100 font-bold bg-black p-6 rounded-xl shadow">Liste des trains</h1>
	</div>

	<!-- Div to list all input filters -->
	<div class="flex flex-col justify-center items-center mt-10">
		<form v-on:submit.prevent="getTrains">
			<div class="flex flex-col">
				<div class="flex items-center justify-center align-center">
					<label for="start" class="mr-5">Date de départ</label>
					<input type="date" id="start" name="tripStart" class="rounded-xl border-2 border-gray-400 p-2" required pattern="[0-9]{4}-[0-9]{2}-[0-9]{2}"
					min="2023-18-01">
				</div>
				<button type="submit" class="bg-green-500 text-white text-xl px-10 py-1.5 mt-5 rounded-full font-medium hover:bg-opacity-75">
					Actualiser
				</button>
			</div>
		</form>
		<!-- Div to list all trains -->
		<div class="flex flex-col justify-center items-center mt-10 overflow-x-auto w-11/12">
			<table class="flex table w-full" id="trains-list">
				<thead class="bg-gray-400">
					<th>Ville de départ</th>
					<th>Départ prévu</th>
					<th>Ville d'arrivée</th>
					<th>Arrivée prévue</th>
					<th>Dispos</th>
					<th>Réserver</th>
				</thead>
				<tr v-for="train in trains.displayJson" :key="train.id" class="bg-gray-100  hover:bg-blue-100"
					@click="">
					<td class="justify-center items-center p-2">{{ train.departure_station }}</td>
					<td>{{ train.departure_date }}</td>
					<td>{{ train.arrival_station }}</td>
					<td>{{ train.arrival_date }}</td>
					<td>{{ train.available_seats }}</td>
					<td class="flex justify-around items-center">
						<router-link :to="{ path: '/reserver', query: { id_train: train.id }}"> 
							<label for="book" class="btn" >
								<Icon icon="mdi:seat" class="text-3xl" />
								
							</label>
						</router-link>
					</td>
				</tr>
			</table>
		</div>
	</div>

</template>