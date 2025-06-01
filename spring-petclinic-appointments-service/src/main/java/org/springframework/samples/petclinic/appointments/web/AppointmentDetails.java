package org.springframework.samples.petclinic.appointments.web;

import java.time.LocalDateTime;

public class AppointmentDetails {
    public Integer id;
    public LocalDateTime appointmentDate;
    public String description;
    public Integer ownerId;
    public Integer petId;
}
