<script setup lang="ts">

import Header from '../../components/Header.vue';
import soapRequest from 'easy-soap-request';

const url = "http://127.0.0.1:8050/"

const train = reactive({
	trainJson: {},
	loading: true
});


const bookTrain = async (event:any) => {
	try {
    event.preventDefault()

		const bookheaders = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'BookTrain',
			'Accept': 'text/xml',
		};

		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:BookTrain>
					<tns:firstName>${event.target.firstName.value}</tns:firstName>
					<tns:lastName>${event.target.lastName.value}</tns:lastName>
					<tns:trainId>${train.trainJson.id}</tns:trainId>
					<tns:passClass>${event.target.class.value}</tns:passClass>
		 		</tns:BookTrain>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

		const { response } = await soapRequest({ url: url, headers: bookheaders, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)

	} catch (e) {
		console.log(e.response.data);
	}
};

const getTrain = async (id:any) => {
	try {
		const header = {
			'Content-Type': 'text/xml;charset=UTF-8',
			'SOAPAction': url + 'GetTrainsById',
			'Accept': 'text/xml',
		};

		const xml =
			`<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://example.com/sample.wsdl">
	 		<soapenv:Body>
		 		<tns:GetTrainsById>
					<tns:id>${id}</tns:id>
		 		</tns:GetTrainsById>
	 		</soapenv:Body>
			</soapenv:Envelope>`;

      const { response } = await soapRequest({ url: url, headers: header, xml: xml, timeout: 1000 }); // Optional timeout parameter(milliseconds)
      const { headers, body, statusCode } = response;
        
      console.log(body)
      train.trainJson = body.substring(body.indexOf("<trainsJson>") + 12, body.indexOf("</trainsJson>"));

		// Parse the string that has &quot
      train.trainJson = JSON.parse(train.trainJson.replace(/&quot;/g, '"'));

      console.log(train.trainJson)

      train.trainJson.departure_date = new Date(Date.parse(train.trainJson.departure_date));
      train.trainJson.arrival_date = new Date(Date.parse(train.trainJson.arrival_date));
      train.trainJson.departure_date =  train.trainJson.departure_date.getDate() +"/"+ train.trainJson.departure_date.getMonth() +"/"+train.trainJson.departure_date.getFullYear()+ " à " + train.trainJson.departure_date.getHours()+":"+train.trainJson.departure_date.getMinutes()
      train.trainJson.arrival_date =  train.trainJson.arrival_date.getDate() +"/"+ train.trainJson.arrival_date.getMonth() +"/"+train.trainJson.arrival_date.getFullYear()+ " à " + train.trainJson.arrival_date.getHours()+":"+train.trainJson.arrival_date.getMinutes()
      console.log(train.trainJson)
      train.loading = false
	} catch (e) {
		console.log(e);
	}
};

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const id_train = urlParams.get('id_train');
  getTrain(id_train)
});


</script>

<template>
    <Header></Header>

    <div class="mt-5 md:col-span-2 md:mt-0">
        <div class="flex flex-col justify-center items-center mt-10">
		    <h1 class="text-4xl font-bold text-gray-800">Réserver</h1>
	    </div>
      <br/>
      <div class="overflow-hidden shadow sm:rounded-md">
        <div class="flex flex-col justify-center items-center mt-10">
          <h3 class="text-2xl font-bold text-gray-800">Train : {{ train.trainJson.departure_station }} - {{ train.trainJson.arrival_station }}</h3>
          <h4 class="text-xl font-bold text-gray-800">Date de départ : {{ train.trainJson.departure_date }} </h4>
          <h4 class="text-xl font-bold text-gray-800">Date d'arrivée :  {{ train.trainJson.arrival_date }} </h4>
        </div>
      </div>
         <form v-on:submit.prevent="bookTrain">
          <div class="overflow-hidden shadow sm:rounded-md">
            <div class="bg-white px-4 py-5 sm:p-6">
                <div class="grid grid-cols-6 gap-6">
                    <div class="col-span-6 sm:col-span-3">
                    <label for="first-name" class="block text-sm font-medium text-gray-700">First name</label>
                    <input type="text" name="firstName" id="first-name" autocomplete="given-name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required/>
                    </div>

                    <div class="col-span-6 sm:col-span-3">
                    <label for="last-name" class="block text-sm font-medium text-gray-700">Last name</label>
                    <input type="text" name="lastName" id="last-name" autocomplete="family-name" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" required/>
                    </div>
                    
                    <div class="col-span-6 sm:col-span-3">
                    <label for="class" class="block text-sm font-medium text-gray-700">Selectionnez votre classe</label>
                    <select id="class" name="class" class="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm">
                        <option value="1">Classe 1 : {{ train.trainJson.nb_class_1 - train.trainJson.current_nb_class_1 }} places restantes au prix de {{ train.trainJson.price_class_1 }} euros</option>
                        <option value="2">Classe 2 : {{ train.trainJson.nb_class_2 - train.trainJson.current_nb_class_2 }} places restantes au prix de {{ train.trainJson.price_class_2 }} euros</option>
                        <option value="3">Classe 3 : {{ train.trainJson.nb_class_3 - train.trainJson.current_nb_class_3 }} places restantes au prix de {{ train.trainJson.price_class_3 }} euros</option>
                    </select>
                    </div>              
                </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 text-center sm:px-6">
              <button type="submit" class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Réserver</button>
            </div>
          </div>
        </form>
      </div>
</template>