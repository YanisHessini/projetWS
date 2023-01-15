<script setup lang="ts">

import Header from '../../components/Header.vue';
import soapRequest from 'easy-soap-request';
import { Icon } from '@iconify/vue';

const url = "http://127.0.0.1:8050/"

const trains = reactive({
	trainsJson: [],
	displayJson: JSON.parse('[]'),
	loading: true
});

// Function to get the list of trains with soap
const getheaders = {
	'Content-Type': 'text/xml;charset=UTF-8',
	'SOAPAction': url + 'GetAllTrains',
	'Accept': 'text/xml',
	'Access-Control-Allow-Origin': '*'
};

const xml =
	`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 	<soapenv:Body>
		 <tns:GetAllTrains/>
	 	</soapenv:Body>
	</soapenv:Envelope>
	`;

const getAllTrains = async () => {
	try {
		const { response } = await soapRequest({ url: url, headers: getheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
		const { headers, body, statusCode } = response;
		console.log(headers);
		console.log(statusCode);

		// Isolate <trainsJson> from the response

		trains.trainsJson = body.substring(body.indexOf("<trainsJson>") + 12, body.indexOf("</trainsJson>"));

		// Parse the string that has &quot

		trains.trainsJson = JSON.parse(trains.trainsJson.replace(/&quot;/g, '"'));
		console.log(trains.trainsJson);

		// Fill displayJson with the columns we want
		// basic number, departure_station, departure_date, arrival_station, arrival_date, total_seats

		for (let i = 0; i < trains.trainsJson.length; i++) {
			trains.displayJson.push({
				"basic_number": i,
				"departure_station": trains.trainsJson[i].departure_station,
				"departure_date": trains.trainsJson[i].departure_date,
				"arrival_station": trains.trainsJson[i].arrival_station,
				"arrival_date": trains.trainsJson[i].arrival_date,
				"total_seats": trains.trainsJson[i].total_seats
			});
		}

		console.log(trains.displayJson);
		trains.loading = false;

	} catch (e) {
		console.log(e.response.data);
	}
};

onMounted(() => {
	getAllTrains();
});

// Function to fill table html with id trains-list with data from JSON


</script>

<template>
	<Header></Header>

	<!-- Welcome text to view the list of trains -->
	<div class="flex flex-col justify-center items-center mt-10">
		<h1 class="text-4xl font-bold text-gray-800">Liste des trains</h1>
	</div>

	<!-- Div to list all input filters -->
	<div class="flex flex-col justify-center items-center mt-10">

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
				<tr v-for="train in trains.displayJson" :key="train.basic_number" class="bg-gray-100  hover:bg-blue-100"
					@click="">
					<td class="justify-center items-center p-2">{{ train.departure_station }}</td>
					<td>{{ train.departure_date }}</td>
					<td>{{ train.arrival_station }}</td>
					<td>{{ train.arrival_date }}</td>
					<td>{{ train.total_seats }}</td>
					<td class="flex justify-around items-center">
						<button>
							<Icon icon="mdi:seat" class="text-3xl" />
						</button>
					</td>
				</tr>
			</table>
		</div>
	</div>


</template>