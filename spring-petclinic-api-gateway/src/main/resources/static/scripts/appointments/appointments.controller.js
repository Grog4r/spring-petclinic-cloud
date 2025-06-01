angular.module('appointments')
    .controller('AppointmentsListController', ['$http', function ($http) {
        var self = this;
        self.appointmentsList = [];

        // Fetch the list of appointments
        $http.get('/api/appointments/appointments')
            .then(function (resp) {
                self.appointmentsList = resp.data;

                self.appointmentsList.forEach(function (appointment) {
                    const ownerId = appointment.ownerId;
                    const petId = appointment.petId;

                    // Initialisiere Owner und Pet, um Fehler im Template zu vermeiden, während die Daten laden
                    appointment.owner = { firstName: 'Loading...', lastName: '' };
                    appointment.pet = { name: 'Loading...' }; // Initialisiere pet ebenfalls
                    appointment.appointmentDate = new Date(appointment.appointmentDate);


                    $http.get(`/api/customer/owners/${ownerId}`)
                        .then(function (ownerResp) {

                            appointment.owner = ownerResp.data;


                            const foundPet = appointment.owner.pets.find(pet => pet.id === petId);

                            if (foundPet) {
                                appointment.pet = foundPet;
                            } else {
                                console.warn(`Pet with ID ${petId} not found for owner ${ownerId} in the fetched owner data.`);
                                appointment.pet = { name: 'Pet not found' };
                            }
                        })
                        .catch(function (err) {
                            console.error(`Failed to fetch owner ${ownerId}:`, err);
                            appointment.owner = { firstName: 'Unknown', lastName: 'Owner' };
                            appointment.pet = { name: 'Unknown Pet' };
                        });

                });
            })
            .catch(function (error) {
                console.error('Failed to fetch appointments:', error);
            });
    }]);