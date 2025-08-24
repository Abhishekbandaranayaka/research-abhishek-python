package com.lungsound.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "audio_clips")
@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class AudioClip {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "users_id", nullable = false, referencedColumnName = "id")
    private User user;

    @Column(name = "file_name",nullable = false)
    private String fileName;

    @Column(name = "prediction")
    private String prediction;

}
