#pragma once

#include <stddef.h>

namespace nexus {

// Charge une seule fois les poids CRDP et le tokenizer CTK2 depuis la Flash
// mappée. Aucun accès SD, USB, Wi-Fi ou réseau n'est nécessaire.
bool nexusLlmRuntimeInit();
bool nexusLlmRuntimeReady();

// Vérifie le budget réel CTK2 avant de lancer une tâche d'inférence.
// Refuse tout prompt qui ne tient pas dans la fenêtre sans le tronquer.
bool nexusLlmRuntimePromptFits(const char* prompt, unsigned maxNewTokens);

// Génère une narration courte en français. Appel à effectuer depuis une
// tâche FreeRTOS dédiée : l'inférence est bloquante pendant le calcul.
bool nexusLlmRuntimeGenerate(const char* prompt, char* output,
                              size_t outputCapacity,
                              unsigned maxNewTokens = 10U);

}  // namespace nexus
