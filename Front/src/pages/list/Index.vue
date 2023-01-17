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
		console.log(e.response.data);
	}
};

const bookTrain = async (id) => {
	try {
		const bookheaders = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'BookTrain',
			'Accept': 'text/xml',
		};

		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:BookTrain>
					<tns:firstName>Yanis</tns:firstName>
					<tns:lastName>Hessini</tns:lastName>
					<tns:trainId>1</tns:trainId>
					<tns:passClass>1</tns:passClass>
		 		</tns:BookTrain>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: bookheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)

		console.log(response.body.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'))

	} catch (e) {
		console.log(e.response.data);
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
				<tr v-for="train in trains.displayJson" :key="train.id" class="bg-gray-100  hover:bg-blue-100"
					@click="">
					<td class="justify-center items-center p-2">{{ train.departure_station }}</td>
					<td>{{ train.departure_date }}</td>
					<td>{{ train.arrival_station }}</td>
					<td>{{ train.arrival_date }}</td>
					<td>{{ train.available_seats }}</td>
					<td class="flex justify-around items-center">
						<label for="book" class="btn" >
							<Icon icon="mdi:seat" class="text-3xl" />
						</label>

						<input v-bind:name="train.id" type="checkbox" id="book" class="modal-toggle"/>
						<label for="book" class="modal cursor-pointer">
							<label class="modal-box relative" for="">
								<h3 v-bind:name="train.id" class="text-lg font-bold">Réserver pour le train</h3>
								
								<div class = "form-control w-full max-w-xs mt-5">
									<label class ="label mt-2">
										<span class="font-bold">Numéro de train</span>
									</label>
										<input type="text" v-bind:placeholder="modal.id" class="input-borderedw-full max-w-xs rounded-lg bg-gray-100" disabled />

									<label class ="label mt-2">
										<span class="font-bold">Départ</span>
									</label>
										<input type="text" class="input-bordered w-full max-w-xs rounded-lg bg-gray-100" disabled />

									<label class ="label mt-2">
										<span class="font-bold">Destination</span>
									</label>
										<input type="text" class="input-bordered w-full max-w-xs rounded-lg bg-gray-100" disabled />

								</div>
								
							</label>
						</label>

					</td>
				</tr>
			</table>
		</div>
	</div>

</template>