<script setup lang="ts">

import Header from '../../components/Header.vue';
import soapRequest from 'easy-soap-request';
const url = "http://127.0.0.1:8050/"


const reservations = reactive({
	reservationsJson: [],
	displayJson: JSON.parse('[]'),
	loading: true
});

const searchReservations = async (event:any) => {
	try {
        event.preventDefault()

        reservations.reservationsJson = []
        reservations.displayJson = JSON.parse('[]')
        reservations.loading = true

		const header = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'GetBookingUser',
			'Accept': 'text/xml',
		};

		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
                <soapenv:Body>
                    <tns:GetBookingUser>
                        <tns:firstName>${event.target.firstName.value}</tns:firstName>
                        <tns:lastName>${event.target.lastName.value}</tns:lastName>
                    </tns:GetBookingUser>
                </soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: header, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
        const { headers, body, statusCode } = response;
        
        console.log(body)
        reservations.reservationsJson = body.substring(body.indexOf("<bookingJson>") + 13, body.indexOf("</bookingJson>"));

		// Parse the string that has &quot
		reservations.reservationsJson = JSON.parse(reservations.reservationsJson.replace(/&quot;/g, '"'));

		// Fill displayJson with the columns we want
		// basic number, departure_station, departure_date, arrival_station, arrival_date, total_seats

		for (let i = 0; i < reservations.reservationsJson.length; i++) {
			reservations.displayJson.push({
                "id_reservation": reservations.reservationsJson[i].id_reservation,
				"id_train": reservations.reservationsJson[i].id_train,
				"departure_station": reservations.reservationsJson[i].departure_station,
				"departure_date": reservations.reservationsJson[i].departure_date,
				"arrival_station": reservations.reservationsJson[i].arrival_station,
				"arrival_date": reservations.reservationsJson[i].arrival_date,
				"class": reservations.reservationsJson[i].class,
			});
		}

		console.log(reservations.displayJson);
		reservations.loading = false;


	} catch (e:any) {
		console.log(e);
	}
};

const cancelBooking = async (id:any) => {
    const header = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'CancelBooking',
			'Accept': 'text/xml',
		};

	const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
                <soapenv:Body>
                    <tns:CancelBooking>
                        <tns:id>${id}</tns:id>
                    </tns:CancelBooking>
                </soapenv:Body>
			</soapenv:Envelope>`;
        
    const { response } = await soapRequest({ url: url, headers: header, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)

    for (let i = 0; i < reservations.displayJson.length; i++) {
        if (reservations.displayJson[i].id_reservation === id) {
            reservations.displayJson.splice(i, 1);
            break;
        }
    }
}

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
        <div v-for="reservation in reservations.displayJson" :key="reservations.id_reservation" class="flex flex-col justify-center items-center mt-10 overflow-x-auto w-11/12">
            <table class="flex table w-full" id="trains-list">
                <thead class="bg-gray-400">
                    <th>Ville de départ</th>
                    <th>Départ prévu</th>
                    <th>Ville d'arrivée</th>
                    <th>Arrivée prévue</th>
                    <th>Classe</th>
                    <th>Annuler</th>
                </thead>
                <tr class="bg-gray-100 ">
                    <td class="justify-center items-center p-2">{{ reservation.departure_station }}</td>
                    <td>{{ reservation.departure_date }}</td>
                    <td>{{ reservation.arrival_station }}</td>
                    <td>{{ reservation.arrival_date }}</td>
                    <td>{{ reservation.class }}</td>
                    <td>
                        <label for="book" class="btn"  @click="cancelBooking(reservation.id_reservation)">
							Annuler
						</label>
                    </td>
                </tr>
            </table>
        </div>
    </div>
</template>