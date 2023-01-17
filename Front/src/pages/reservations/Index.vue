<script setup lang="ts">

import Header from '../../components/Header.vue';
import soapRequest from 'easy-soap-request';
const url = "http://127.0.0.1:8050/"


const trains = reactive({
	trainsJson: [],
	displayJson: JSON.parse('[]'),
	loading: true
});

const searchReservations = async (event:any) => {
	try {
        event.preventDefault()

		const bookheaders = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'GetTrainsSearchUser',
			'Accept': 'text/xml',
		};

		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:GetTrainsSearchUser>
					<tns:firstName>${event.target.firstName.value}</tns:firstName>
					<tns:lastName>${event.target.lastName.value}</tns:lastName>
		 		</tns:GetTrainsSearchUser>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: bookheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
        const { headers, body, statusCode } = response;
        
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
				"class": trains.trainsJson[i].class,
			});
		}

		console.log(trains.displayJson);
		trains.loading = false;


	} catch (e:any) {
		console.log(e);
	}
};

</script>

<template>
    <Header></Header>

    <div class="mt-5 md:col-span-2 md:mt-0">
        <div class="flex flex-col justify-center items-center mt-10">
		    <h1 class="text-4xl font-bold text-gray-800">Réservations</h1>
	    </div>
        <form v-on:submit.prevent="searchReservations">
          <div class="overflow-hidden shadow sm:rounded-md">
            <div class="bg-white px-4 py-5 sm:p-6">
                <div class="grid grid-cols-6 gap-6">
                    <div class="col-span-6 sm:col-span-3">
                    <label for="first-name" class="block text-sm font-medium text-gray-700">First name</label>
                    <input type="text" name="firstName" id="first-name" autocomplete="given-name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
                    </div>

                    <div class="col-span-6 sm:col-span-3">
                    <label for="last-name" class="block text-sm font-medium text-gray-700">Last name</label>
                    <input type="text" name="lastName" id="last-name" autocomplete="family-name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" />
                    </div>            
                </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 text-center sm:px-6">
              <button type="submit" class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Voir mes réservations</button>
            </div>
          </div>
        </form>

    </div>
    <div class="flex flex-col justify-center items-center mt-10">
        <div v-for="train in trains.displayJson" :key="train.id" class="flex flex-col justify-center items-center mt-10 overflow-x-auto w-11/12">
            <table class="flex table w-full" id="trains-list">
                <thead class="bg-gray-400">
                    <th>Ville de départ</th>
                    <th>Départ prévu</th>
                    <th>Ville d'arrivée</th>
                    <th>Arrivée prévue</th>
                    <th>Classe</th>
                </thead>
                <tr class="bg-gray-100  hover:bg-blue-100" @click="">
                    <td class="justify-center items-center p-2">{{ train.departure_station }}</td>
                    <td>{{ train.departure_date }}</td>
                    <td>{{ train.arrival_station }}</td>
                    <td>{{ train.arrival_date }}</td>
                    <td>{{ train.class }}</td>
                </tr>
            </table>
        </div>
    </div>
</template>