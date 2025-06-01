package org.springframework.samples.petclinic.appointments.web.mapper;

import org.springframework.samples.petclinic.appointments.model.Appointment;
import org.springframework.samples.petclinic.appointments.web.AppointmentDetails;
import org.springframework.samples.petclinic.appointments.web.AppointmentRequest;

public class AppointmentMapper {

    public static AppointmentDetails toDetails(Appointment entity) {
        AppointmentDetails dto = new AppointmentDetails();
        dto.id = entity.getId();
        dto.appointmentDate = entity.getAppointmentDate();
        dto.description = entity.getDescription();
        dto.ownerId = entity.getOwnerId();
        dto.petId = entity.getPetId();
        return dto;
    }

    public static Appointment toEntity(AppointmentRequest request) {
        Appointment entity = new Appointment();
        entity.setAppointmentDate(request.appointmentDate);
        entity.setDescription(request.description);
        entity.setOwnerId(request.ownerId);
        entity.setPetId(request.petId);
        return entity;
    }
}
