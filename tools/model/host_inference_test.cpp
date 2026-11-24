#include "llm.h"

#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <vector>

static bool readBinary(const char* path, std::vector<uint8_t>& bytes) {
  std::ifstream input(path, std::ios::binary);
  if (!input) return false;
  bytes.assign(std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>());
  return !bytes.empty();
}

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "Usage: host_inference_test MODEL.bin TOKENIZER.bin\n";
    return 2;
  }

  std::vector<uint8_t> model;
  std::vector<uint8_t> tokenizerBlob;
  if (!readBinary(argv[1], model) || !readBinary(argv[2], tokenizerBlob)) {
    std::cerr << "Impossible de lire les deux assets du narrateur.\n";
    return 2;
  }

  Transformer transformer{};
  if (!llm_init_embedded(&transformer, model.data(), model.size(), 32)) {
    std::cerr << "Le moteur hôte refuse le modèle CRDP v3.\n";
    return 1;
  }

  auto fail = [&](const char* message) {
    std::cerr << message << "\n";
    llm_free(&transformer);
    return 1;
  };

  if (transformer.config.arch != ARCH_LLAMA ||
      transformer.config.vocab_size <= 0 ||
      transformer.kv_seq_len != 32) {
    return fail("Architecture, vocabulaire ou contexte du modèle inattendus.");
  }

  Tokenizer tokenizer{};
  if (!llm_tokenizer_from_memory(&tokenizer, tokenizerBlob.data(),
                                 tokenizerBlob.size(),
                                 transformer.config.vocab_size)) {
    return fail("Le moteur hôte refuse le tokenizer CTK2.");
  }
  if (tokenizer.style != ARCH_GPTNEO || tokenizer.eos_id < 0 ||
      tokenizer.eos_id >= tokenizer.vocab_size) {
    return fail("Les métadonnées CTK2 ne correspondent pas au profil attendu.");
  }

  const std::string prompt = "User: Le relais 07 emet trois impulsions.\nBot:";
  int tokens[64] = {};
  int tokenCount = 0;
  llm_encode(&tokenizer, prompt.c_str(), 1, 0, tokens, &tokenCount);
  if (tokenCount < 2 || tokenCount > 23) {
    return fail("Le prompt de contrôle dépasse le budget de contexte de 32 tokens.");
  }

  float* logits = nullptr;
  for (int position = 0; position < tokenCount; ++position) {
    logits = llm_forward(&transformer, tokens[position], position);
    if (!logits) return fail("llm_forward a échoué pendant le pré-remplissage du prompt.");
  }
  for (int i = 0; i < transformer.config.vocab_size; ++i) {
    if (!std::isfinite(logits[i])) {
      return fail("Le moteur a produit un logit non fini.");
    }
  }

  Sampler sampler{};
  llm_build_sampler(&sampler, tokenizer.vocab_size, 0.0f, 1.0f, 0x4E45585553ULL);
  int previous = tokens[tokenCount - 1];
  int position = tokenCount;
  size_t decodedBytes = 0;
  unsigned generatedTokens = 0;

  // Argmax deterministe : trois pas maximum suffisent à prouver le chemin
  // complet logits -> sampler -> CTK2 decoder sans prétendre valider le style.
  for (unsigned step = 0; step < 3 && position < 32; ++step) {
    const int next = llm_sample(&sampler, logits);
    if (next < 0 || next >= tokenizer.vocab_size) {
      return fail("Le sampler a retourné un identifiant hors vocabulaire.");
    }
    ++generatedTokens;
    if (next == tokenizer.eos_id) break;

    char scratch[512] = {};
    const char* piece = llm_decode(&tokenizer, previous, next,
                                   scratch, sizeof(scratch));
    if (!piece) return fail("Le décodeur CTK2 a retourné un pointeur nul.");
    decodedBytes += std::char_traits<char>::length(piece);
    previous = next;
    ++position;
    if (step + 1 < 3 && position < 32) {
      logits = llm_forward(&transformer, next, position - 1);
      if (!logits) return fail("llm_forward a échoué pendant la génération.");
    }
  }

  llm_free(&transformer);
  if (generatedTokens == 0) {
    std::cerr << "Aucun token de sortie n'a été produit.\n";
    return 1;
  }
  std::cout << "NEXUS HOST INFERENCE PASS: CRDP v3 + CTK2 chargés, "
            << tokenCount << " tokens de prompt, "
            << generatedTokens << " token(s) échantillonné(s), "
            << decodedBytes << " octet(s) décodé(s).\n";
  return 0;
}
