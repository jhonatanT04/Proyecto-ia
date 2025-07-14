import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [RouterModule,CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  
  diseases:any = [
  {
    name: "Atelectasis",
    explanation: "Colapso parcial o total del pulmón o de una parte de él. Puede causar dificultad para respirar y niveles bajos de oxígeno."
  },
  {
    name: "Consolidation",
    explanation: "Condensación del tejido pulmonar debido a la acumulación de líquido, generalmente asociada a neumonía."
  },
  {
    name: "Infiltration",
    explanation: "Presencia de sustancias anormales en el tejido pulmonar, indicando inflamación o infección."
  },
  {
    name: "Pneumothorax",
    explanation: "Acumulación de aire en el espacio pleural que provoca el colapso del pulmón."
  },
  {
    name: "Edema",
    explanation: "Acumulación de líquido en los pulmones, comúnmente causada por insuficiencia cardíaca."
  },
  {
    name: "Emphysema",
    explanation: "Enfermedad pulmonar crónica que destruye los alvéolos y dificulta la respiración."
  },
  {
    name: "Fibrosis",
    explanation: "Formación de tejido cicatricial en los pulmones que reduce su flexibilidad y función."
  },
  {
    name: "Effusion",
    explanation: "Acumulación excesiva de líquido en la cavidad pleural alrededor de los pulmones."
  },
  {
    name: "Pneumonia",
    explanation: "Infección que inflama los sacos de aire de uno o ambos pulmones, llenándolos de líquido o pus."
  },
  {
    name: "Pleural_Thickening",
    explanation: "Engrosamiento de la pleura (revestimiento de los pulmones) que puede restringir la respiración."
  },
  {
    name: "Cardiomegaly",
    explanation: "Agrandamiento anormal del corazón, a menudo relacionado con enfermedades cardíacas crónicas."
  },
  {
    name: "Nodule",
    explanation: "Pequeña masa anormal en el pulmón que puede ser benigna o indicar cáncer."
  },
  {
    name: "Mass",
    explanation: "Lesión más grande que un nódulo, que podría representar un tumor benigno o maligno."
  },
  {
    name: "Hernia",
    explanation: "Protrusión de un órgano a través de una abertura anormal, por ejemplo, una hernia diafragmática."
  },
  {
    name: "Lung Lesion",
    explanation: "Área de tejido pulmonar dañada o anormal que puede indicar infección, inflamación o cáncer."
  },
  {
    name: "Fracture",
    explanation: "Hueso roto o fisura visible en la radiografía de tórax, generalmente de costillas."
  },
  {
    name: "Lung Opacity",
    explanation: "Área densa o blanca en la radiografía, indicando acumulación de líquido, infección o inflamación."
  },
  {
    name: "Enlarged Cardiomediastinum",
    explanation: "Agrandamiento de la región media del tórax (cardiomediastino), que puede indicar enfermedades del corazón o grandes vasos."
  }
];
  selectedDisease: any = {
    name: "",
    explanation: "Esta práctica de Inteligencia Artificial utiliza el conjunto de datos ChestX-ray8, el cual contiene más de 100,000 radiografías frontales del tórax. Mediante modelos de aprendizaje profundo, se realiza una detección automática de enfermedades torácicas como Atelectasia, Cardiomegalia, Derrame pleural, Infiltración, Masa, Nódulo, Neumonía y Neumotórax. El sistema ha sido entrenado con una red neuronal convolucional (CNN) para realizar clasificación multietiqueta y localizar regiones afectadas de forma débilmente supervisada. El objetivo es construir una herramienta de apoyo diagnóstico a gran escala que pueda ser usada en entornos hospitalarios."
  };
  selctDefect(){
    this.selectedDisease= {
    name: "",
    explanation: "Esta práctica de Inteligencia Artificial utiliza el conjunto de datos ChestX-ray8, el cual contiene más de 100,000 radiografías frontales del tórax. Mediante modelos de aprendizaje profundo, se realiza una detección automática de enfermedades torácicas como Atelectasia, Cardiomegalia, Derrame pleural, Infiltración, Masa, Nódulo, Neumonía y Neumotórax. El sistema ha sido entrenado con una red neuronal convolucional (CNN) para realizar clasificación multietiqueta y localizar regiones afectadas de forma débilmente supervisada. El objetivo es construir una herramienta de apoyo diagnóstico a gran escala que pueda ser usada en entornos hospitalarios."
  };
  }
  selectDisease(disease: any) {
    this.selectedDisease = disease;
  }
}
