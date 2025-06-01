package org.springframework.samples.petclinic.appointments.web;

import java.time.LocalDateTime;

public class AppointmentRequest {
    public LocalDateTime appointmentDate;
    public String description;
    public Integer ownerId;
    public Integer petId;
}
