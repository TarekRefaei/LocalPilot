/**
 * @deprecated Act v1 is deprecated.
 * Use Execute (v2) pipeline instead.
 */
import type { Plan } from '../../core/entities/plan.entity';

export class ActService {
  private disabled(): never {
    throw new Error('Act v1 is deprecated and disabled.');
  }

  start(_plan: Plan): never { return this.disabled(); }
  run(): never { return this.disabled(); }
  pause(): never { return this.disabled(); }
  resume(): never { return this.disabled(); }
  async runTask(): Promise<never> { return this.disabled(); }
  async runAll(): Promise<never> { return this.disabled(); }
  skip(): never { return this.disabled(); }
  cancel(): never { return this.disabled(); }
}
