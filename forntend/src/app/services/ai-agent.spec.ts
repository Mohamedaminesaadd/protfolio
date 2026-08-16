import { TestBed } from '@angular/core/testing';

import { AiAgent } from './ai-agent';

describe('AiAgent', () => {
  let service: AiAgent;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AiAgent);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
