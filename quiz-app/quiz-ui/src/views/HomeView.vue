<script setup>
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
</script>

<template>
  <section class="p-8 space-y-4">
    <Card>
      <CardHeader><CardTitle>Quiz UI — Ocean Breeze</CardTitle></CardHeader>
      <CardContent class="space-x-2">
        <Button>Primary</Button>
        <Button variant="secondary">Secondary</Button>
      </CardContent>
    </Card>
  </section>
</template>

