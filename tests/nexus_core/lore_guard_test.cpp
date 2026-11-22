#include "nexus_lore_guard.h"
#include <assert.h>
int main() {
  assert(!nexus::containsLegacyFictionReference("LIA archive un echo a Valbrume."));
  assert(!nexus::containsLegacyFictionReference("La Rémanence produit trois impulsions."));
  assert(nexus::containsLegacyFictionReference("Un signal vient de Hawkins."));
  assert(nexus::containsLegacyFictionReference("The Upside Down appears."));
  assert(nexus::containsLegacyFictionReference("Une trace de Demogorgon."));
  return 0;
}
