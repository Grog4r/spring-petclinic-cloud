angular.module('appointmentForm')
    .controller('AppointmentFormController', ['$http', '$state', function ($http, $state) {
        var self = this;

        // Form fields
        self.owners = [];
        self.pets = [];
        self.selectedOwnerId = null;
        self.selectedPetId = null;
        self.appointmentDate = '';
        self.description = '';
        self.loadingPets = false;
        self.errorMessage = '';

        // Load all owners
        $http.get('/api/customer/owners')
            .then(function (response) {
                console.log('Raw owners data:', response.data);
                self.owners = response.data;
                console.log('Assigned owners:', self.owners); // <-- Should match above
            })
            .catch(function (error) {
                console.error('Failed to load owners', error);
                self.errorMessage = 'Failed to load owners. Please try again.';
            });

        // Load pets for selected owner
        self.onOwnerSelected = function () {
            self.pets = [];
            self.selectedPetId = null;

            if (!self.selectedOwnerId) return;

            self.loadingPets = true;

            $http.get('/api/customer/owners/' + self.selectedOwnerId)
                .then(function (response) {
                    console.log('Raw owners data:', response.data);
                    self.pets = response.data.pets || [];
                })
                .catch(function (error) {
                    console.error('Failed to load pets', error);
                    self.errorMessage = 'Failed to load pets for this owner.';
                })
                .finally(function () {
                    self.loadingPets = false;
                });
        };

        // Submit form
        self.submitAppointmentForm = function () {
            self.errorMessage = '';

            if (!self.selectedOwnerId) {
                self.errorMessage = 'Please select an owner.';
                return;
            }

            if (!self.selectedPetId) {
                self.errorMessage = 'Please select a pet.';
                return;
            }

            if (!self.appointmentDate) {
                self.errorMessage = 'Please select an appointment date.';
                return;
            }

            var appointmentData = {
                ownerId: self.selectedOwnerId,
                petId: self.selectedPetId,
                appointmentDate: self.appointmentDate,
                description: self.description
            };

            $http.post('/api/appointments/appointments/new', appointmentData)
                .then(function () {
                    $state.go('appointments');
                })
                .catch(function (error) {
                    console.error('Failed to create appointment', error);
                    self.errorMessage = 'Failed to create appointment. Please try again.';
                });
        };
    }]);